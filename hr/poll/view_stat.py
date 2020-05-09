from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


from .models import Poll, UserProfile, Question, CheckedQuestion, CheckedAnswer, CheckedPoll, Poll, Answer


def get_stat(request):
    save_valid_stat()
    answer_stat()
    question_stat()
    poll_stat()
    return redirect(reverse_lazy('poll:index'))

def poll_stat():
    for poll in Poll.objects.all():
        checked_poll_count = CheckedPoll.objects.filter(poll__pk=poll.pk).count()
        valid_poll_count = CheckedPoll.objects.filter(poll__pk=poll.pk, valid=True).count()
        poll.checked_count = checked_poll_count
        poll.valid_count = valid_poll_count
        poll.save()

def question_stat():
    for question in Question.objects.all():
        checked_question_count = CheckedQuestion.objects.filter(question__pk=question.pk).count()
        valid_question_count = CheckedQuestion.objects.filter(question__pk=question.pk, valid=True).count()
        question.checked_count = checked_question_count
        question.valid_count = valid_question_count
        question.save()
        

def answer_stat():
    for answer in Answer.objects.all():
        
        checked_answers_count = answer.checked_answers.filter(checked=True).count() # Сколько раз отмечали данный ответ верным
        valid_answers_count = answer.checked_answers.filter(valid=True).count() # Сколько раз ответ был верным
        answer.checked_count = checked_answers_count
        answer.valid_count = valid_answers_count
        answer.save()

def save_valid_stat():
    """
    Подготовка базы к обработке
    Проверяем валидность всех опросов, вопросов и ответов
    Заполняем незаполненные поля пустыми значениями
    """

    # Проверяем валидность всех пройденных опросов
    checked_polls = CheckedPoll.objects.filter(checked=True)
    checked_poll_valid = True
    for checked_poll in checked_polls:

        # Создаем незавершенные вопросы завершенного опроса
        poll = Poll.objects.get(pk=checked_poll.poll.pk)
        for question in poll.questions.all():
            check = False
            for checked_question in checked_poll.questions.all():
                if question.pk == checked_question.question.pk:
                    check = True
            if check == False:
                CheckedQuestion.objects.create(question=question, poll=checked_poll)

        # Проверяем валидность всех пройденных вопросов в пройденном опросе
        checked_questions = CheckedQuestion.objects.filter(poll=checked_poll)
        for checked_question in checked_questions:

            # Проверяем наличие ответов и в случае отсутствия заносим в базу пустые значения
            if checked_question.answers.all().count() == 0:
                question = Question.objects.get(pk=checked_question.question.pk)
                for answer in question.answers.all():
                    CheckedAnswer.objects.create(answer=answer, checked='False', question=checked_question)

            # Проверяем правильность ответов, записываем в базу и производим подсчет правильных ответов
            checked_question_valid = True
            for checked_answer in checked_question.answers.all():
                
                # Устанавливаем валидность ответа
                if checked_answer.checked == checked_answer.answer.valid and poll.test:
                    checked_answer.valid = True
                else:
                    checked_answer.valid = False
                    checked_question_valid = False
                checked_answer.save()
                
            # Устанавливаем валидность вопроса
            if checked_question_valid:
                checked_question.valid = True
            else:
                checked_question.valid = False
                checked_poll_valid = False
            checked_question.save()

        # Устанавливаем валидность опроса
        if checked_poll_valid:
            checked_poll.valid = True
        else:
            checked_poll.valid = False
        checked_poll.save()
        