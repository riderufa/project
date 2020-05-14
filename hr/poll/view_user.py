from django.shortcuts import render, redirect
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.views.generic.detail import SingleObjectMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# from django.forms import modelformset_factory
from django.contrib import messages

import redis
import pickle

from datetime import date

# from .forms import PollForm, PollSetForm, KitForm, CheckedAnswerForm
from .models import Poll, UserProfile, Question, CheckedQuestion, CheckedAnswer, CheckedPoll


"""
Контроллеры пользователя
"""

cache = redis.Redis(host='REDIS_URL', port=6379)


@login_required
def check_poll(request, pk):
    """
    Получаем список вопросов по конкретному опросу для конкретного пользователя
    """
    poll = Poll.objects.get(pk=pk)
    user = UserProfile.objects.get(user=request.user)

    # Проверка доступности опроса по дате
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
    
    # опрос не начинали проходить
    if not poll_pk: 
        # Проверка одновременности опросов
        for key in cache.keys():
            if key.decode('utf-8').endswith('u' + str(request.user.pk) + 'time'):
                messages.add_message(request, messages.INFO, 'Вы должны закончить ранее начатый опрос.', extra_tags='alert-danger')
                return redirect(reverse_lazy('poll:index'))
        cache.set(f'p{new_poll.pk}u{request.user.pk}', pickle.dumps(new_poll.pk)) # Сохранем в redis метку начала прохождения опроса (хранится постоянно)
        cache.set(f'pu{request.user.pk}', pickle.dumps(new_poll.pk)) # Сохраняем в redis pk объекта CheckedPoll (хранится только в сессии)
        cache.set(f'p{new_poll.pk}u{request.user.pk}time', pickle.dumps(new_poll.pk), ex=poll.time_limit) # , ex=poll.time_limit # Сохраняем в redis pk объекта CheckedPoll со временем (хранится до окончания опроса)

    elif not cache.get(f'p{new_poll.pk}u{request.user.pk}time'): # опрос начинали проходить, но время закончилось
        messages.add_message(request, messages.INFO, 'Время, выделенное на опрос закончилось.', extra_tags='alert-danger')
        return redirect(reverse_lazy('poll:index'))

    # Рендерим список вопросов и давляем в контекст время
    questions = Question.objects.filter(polls__pk=pk)
    ttl_poll = cache.ttl(f'p{new_poll.pk}u{request.user.pk}time')
    return render(request, 'poll/user/check_poll.html', context={'questions': questions, 'ttl_poll': ttl_poll, 'new_poll_pk': new_poll.pk})


@login_required
def question_get_answer(request, pk):
    """
    Получаем список ответов по конкретному вопросу по конкретному опросу для конкретного пользователя
    """
    poll_pk = pickle.loads(cache.get(f'pu{request.user.pk}')) # Получаем из redis pk объекта CheckedPoll
    question = Question.objects.get(pk=pk)
    poll = CheckedPoll.objects.get(pk=poll_pk)
    
    # Создаем или получаем созданый ранее объект CheckedQuestion
    if CheckedQuestion.objects.filter(poll=poll, question=question).first():
        new_question = CheckedQuestion.objects.get(poll=poll, question=question)
    else:
        new_question = CheckedQuestion.objects.create(question=question, poll=poll)
    
    # Проверка наличия в redis метки начала прохождения вопроса
    question_pk = cache.get(f'q{new_question.pk}p{poll_pk}u{request.user.pk}')
    
    if not question_pk: # вопрос не начинали проходить
        cache.set(f'q{new_question.pk}p{poll_pk}u{request.user.pk}', pickle.dumps(new_question.pk)) # Сохранем в redis метку начала прохождения вопроса (хранится постоянно)
        cache.set(f'qu{request.user.pk}', pickle.dumps(new_question.pk)) # Сохраняем в redis pk объекта CheckedQuestion (хранится только в сессии)
        cache.set(f'q{new_question.pk}p{poll_pk}u{request.user.pk}time', pickle.dumps(new_question.pk), ex=question.time_limit) # , ex=question.time_limit # Сохраняем в redis pk объекта QuestionPoll со временем (хранится до окончания вопроса)

    # Проверка вопроса по времени
    elif not cache.get(f'q{new_question.pk}p{poll_pk}u{request.user.pk}time'):
        messages.add_message(request, messages.INFO, 'Время получения ответа на вопрос прошло.', extra_tags='alert-danger')
        return redirect(reverse_lazy('poll:user_question_list', kwargs={'pk': poll.poll.pk}))
    
    # Рендерим список ответов и добавляем в контекст информацию
    return_path  = request.META.get('HTTP_REFERER','/') # Сохранем метку возврата на предыдущую страницу
    question = Question.objects.prefetch_related('answers').get(pk=pk)
    ttl_question = cache.ttl(f'q{new_question.pk}p{poll_pk}u{request.user.pk}time') # Время вопроса
    ttl_poll = cache.ttl(f'p{poll.pk}u{request.user.pk}time') # Время опроса
    context = {'question': question, 'return_path': return_path, 'pk': pk, 'ttl_question': ttl_question, 'ttl_poll': ttl_poll}
    if CheckedQuestion.objects.filter(poll=poll, question=question).first():
        new_question = CheckedQuestion.objects.prefetch_related('answers').prefetch_related('answers__answer').get(poll=poll, question=question)
        context['answers'] = new_question.answers.all() #.select_related('answer')
    return render(request, 'poll/user/question_get_answer.html', context=context)


@login_required
def add_answers(request):
    """
    Создаем ответы на вопрос
    """
    checked = request.GET['checked'] # Получаем строку с отметками ответов
    pk = request.GET['pk']
    newpk = pickle.loads(cache.get(f'qu{request.user.pk}'))
    checked_question = CheckedQuestion.objects.get(pk=newpk)
    question = Question.objects.prefetch_related('answers').get(pk=pk)
    i = 0
    
    # Создаем или переписываем новыми данными ответ
    for answer in question.answers.all():
        checked_answer = CheckedAnswer.objects.filter(answer=answer, question=checked_question).first()
        if checked_answer:
            checked_answer.checked = checked[i]
            checked_answer.save()
        else:
            CheckedAnswer.objects.create(answer=answer, checked=checked[i], question=checked_question)
        i += 1

    return redirect(reverse_lazy('poll:index'))
 