from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.contrib import messages

import redis
import pickle

from datetime import date

from .forms import PollForm, PollSetForm, KitForm, CheckedAnswerForm
from .models import Poll, UserProfile, Question, CheckedQuestion, CheckedAnswer, CheckedPoll

cache = redis.Redis(host='127.0.0.1', port=6379)

@login_required
def user_question_list(request, pk):
    """
    Получаем список вопросов по конкретному опросу для конкретного пользователя
    """
    
    

    poll = Poll.objects.get(pk=pk)
    user = UserProfile.objects.get(user=request.user)

    if poll.date_pub > date.today():
        messages.add_message(request, messages.INFO, f'Дата проведение опроса {poll.date_pub} еще не наступила', extra_tags='alert-danger')
        return redirect(reverse_lazy('poll:index'))

    # Создаем или получаем созданый ранее объект CheckedPoll
    if CheckedPoll.objects.filter(poll=poll, user=user).first():
        new_poll = CheckedPoll.objects.get(poll=poll, user=user)
    else:
        new_poll = CheckedPoll.objects.create(poll=poll, user=user)
    
    # Проверка наличия в redis метки начала прохождения опроса
    poll_pk = cache.get(f'p{new_poll.pk}u{request.user.pk}')
    
    if not poll_pk: # опрос не начинали проходить
        cache.set(f'p{new_poll.pk}u{request.user.pk}', pickle.dumps(new_poll.pk)) # Сохранем в redis метку начала прохождения опроса (хранится постоянно)
        cache.set(f'pu{request.user.pk}', pickle.dumps(new_poll.pk)) # Сохраняем в redis pk объекта CheckedPoll (хранится только в сессии)
        cache.set(f'p{new_poll.pk}u{request.user.pk}time', pickle.dumps(new_poll.pk), ex=poll.time_limit) # , ex=poll.time_limit # Сохраняем в redis pk объекта CheckedPoll со временем (хранится до окончания опроса)

    elif not cache.get(f'p{new_poll.pk}u{request.user.pk}time'): # опрос начинали проходить, но время закончилось
        new_poll.checked = True # Устанавливаем опрос завершенным
        new_poll.save()
        messages.add_message(request, messages.INFO, 'Время, выделенное на опрос закончилось.', extra_tags='alert-danger')
        return redirect(reverse_lazy('poll:index'))

    # Рендерим список вопросов
    questions = Question.objects.filter(polls__pk=pk)
    ttl_poll = cache.ttl(f'p{new_poll.pk}u{request.user.pk}time')
    return render(request, 'poll/user/user_question_list.html', context={'questions': questions, 'ttl_poll': ttl_poll})


def question_get_answer(request, pk):
    """
    Получаем список ответов по конкретному вопросу по конкретному опросу для конкретного пользователя
    """
    poll_pk = pickle.loads(cache.get(f'pu{request.user.pk}')) # Получаем из redis pk объекта CheckedPoll
    # cache.set(f'pk{request.user.pk}', pickle.dumps(pk))

    # if poll.date_pub > date.today():
    #     print(123)


    # print(poll_pk)
    # poll_id = cache.get('adverts')
    # if adverts:
    #     adverts_value = pickle.loads(adverts)
    # else:
    #     adverts_value = Advert.objects.all()
    #     cache.set(f`poll{pk}user`, pickle.dumps(adverts_value))

    # Создаем или получаем созданый ранее объект CheckedQuestion
    question = Question.objects.get(pk=pk)
    poll = CheckedPoll.objects.get(pk=poll_pk)

    

    if CheckedQuestion.objects.filter(poll=poll, question=question).first():
        new_question = CheckedQuestion.objects.get(poll=poll, question=question)
        # print(new_question.answers.all().count())
        # if new_question.answers.all().count() != 0:
        #     messages.add_message(request, messages.INFO, 'Вы уже ответили на этот вопрос.', extra_tags='alert-danger')
        #     return redirect(reverse_lazy('poll:user_question_list', kwargs={'pk': poll.poll.pk}))
    else:
        new_question = CheckedQuestion.objects.create(question=question, poll=poll)
    
    # Проверка наличия в redis метки начала прохождения вопроса
    question_pk = cache.get(f'q{new_question.pk}p{poll_pk}u{request.user.pk}')
    
    if not question_pk: # вопрос не начинали проходить
        cache.set(f'q{new_question.pk}p{poll_pk}u{request.user.pk}', pickle.dumps(new_question.pk)) # Сохранем в redis метку начала прохождения вопроса (хранится постоянно)
        cache.set(f'qu{request.user.pk}', pickle.dumps(new_question.pk)) # Сохраняем в redis pk объекта CheckedQuestion (хранится только в сессии)
        cache.set(f'q{new_question.pk}p{poll_pk}u{request.user.pk}time', pickle.dumps(new_question.pk), ex=question.time_limit) # , ex=question.time_limit # Сохраняем в redis pk объекта QuestionPoll со временем (хранится до окончания вопроса)

    elif not cache.get(f'q{new_question.pk}p{poll_pk}u{request.user.pk}time'):
        messages.add_message(request, messages.INFO, 'Время получения ответа на вопрос прошло.', extra_tags='alert-danger')
        return redirect(reverse_lazy('poll:user_question_list', kwargs={'pk': poll.poll.pk}))
    
    # Рендерим список ответов
    return_path  = request.META.get('HTTP_REFERER','/') # Сохранем метку возврата на предыдущую страницу
    question = Question.objects.get(pk=pk)
    ttl_question = cache.ttl(f'q{new_question.pk}p{poll_pk}u{request.user.pk}time')
    ttl_poll = cache.ttl(f'p{poll.pk}u{request.user.pk}time')
    context = {'question': question, 'return_path': return_path, 'pk': pk, 'ttl_question': ttl_question, 'ttl_poll': ttl_poll}
    if CheckedQuestion.objects.filter(poll=poll, question=question).first():
        new_question = CheckedQuestion.objects.get(poll=poll, question=question)
        context['answers'] = new_question.answers.all()
    
    
    return render(request, 'poll/user/question_get_answer.html', context=context)

def add_answers(request):
    checked = request.GET['checked'] # Получаем строку с отметками ответов
    pk = request.GET['pk']
    # newpk = request.GET['newpk']
    newpk = pickle.loads(cache.get(f'qu{request.user.pk}'))
    checked_question = CheckedQuestion.objects.get(pk=newpk)
    question = Question.objects.get(pk=pk)
    i = 0
    
    for answer in question.answers.all():
        checked_answer = CheckedAnswer.objects.filter(answer=answer, question=checked_question).first()
        if checked_answer:
            checked_answer.checked = checked[i]
            checked_answer.save()
        else:
            CheckedAnswer.objects.create(answer=answer, checked=checked[i], question=checked_question)
        i += 1

    # messages.add_message(request, messages.INFO, 'Ответ на вопрос получен')

    return redirect(reverse_lazy('poll:index'))
    # questions = Question.objects.filter(polls__pk=question.poll.poll.pk)
    # return redirect(request, 'poll/user/user_question_list.html', context={'questions': questions})
    # return '123'

# def question_get_answer1(request, pk):
#     # pass
#     question = Question.objects.get(pk=pk)
#     answers = question.answers.all()
#     l = answers.count()
#     print(l)
#     AnswerFormSet = modelformset_factory(CheckedAnswer, form=CheckedAnswerForm, extra=l)

#     if request.method == 'POST':
#         formset = AnswerFormSet(request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect('poll:index')
#     else:
#         formset = AnswerFormSet()
#     context = {'formset': formset, 'answers': answers}
#     return render(request, 'poll/user/question_get_answer1.html', context)