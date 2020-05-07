from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.forms import modelformset_factory

import redis
import pickle

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

    # Создаем или получаем созданый ранее объект CheckedPoll
    if CheckedPoll.objects.filter(poll=poll, user=user).first():
        new_poll = CheckedPoll.objects.get(poll=poll, user=user)
    else:
        new_poll = CheckedPoll.objects.create(poll=poll, user=user)
    
    # Проверка наличия в redis метки начала прохождения опроса
    poll_pk = cache.get(f'poll{new_poll.pk}user{request.user.pk}')
    
    if not poll_pk: # опрос не начинали проходить
        cache.set(f'poll{new_poll.pk}user{request.user.pk}', pickle.dumps(new_poll.pk)) # Сохранем в redis метку начала прохождения опроса
        cache.set(f'polluser{request.user.pk}', pickle.dumps(new_poll.pk)) # , ex=poll.time_limit # Сохраняем в redis pk объекта CheckedPoll со временем жизни

    elif not cache.get(f'polluser{request.user.pk}'): # опрос начинали проходить, но время жизни закончилось
        return redirect(reverse_lazy('poll:index'))

    # Рендерим список вопросов
    questions = Question.objects.filter(polls__pk=pk)
    return render(request, 'poll/user/user_question_list.html', context={'questions': questions})


def question_get_answer(request, pk):
    """
    Получаем список ответов по конкретному вопросу по конкретному опросу для конкретного пользователя
    """
    poll_pk = pickle.loads(cache.get(f'polluser{request.user.pk}')) # Получаем из redis pk объекта CheckedPoll
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
    else:
        new_question = CheckedQuestion.objects.create(question=question, poll=poll)
    
    # Проверка наличия в redis метки начала прохождения вопроса
    question_pk = cache.get(f'question{new_question.pk}poll{poll_pk}user{request.user.pk}')
    
    if not question_pk: # вопрос не начинали проходить
        cache.set(f'question{new_question.pk}poll{poll_pk}user{request.user.pk}', pickle.dumps(new_question.pk))
        cache.set(f'questionuser{request.user.pk}', pickle.dumps(new_question.pk)) # , ex=poll.time_limit

    elif not cache.get(f'user{request.user.pk}'):
        return redirect(reverse_lazy('poll:index'))
    
    # Рендерим список ответов
    return_path  = request.META.get('HTTP_REFERER','/') # Сохранем метку возврата на предыдущую страницу
    question = Question.objects.get(pk=pk)
    return render(request, 'poll/user/question_get_answer.html', context={'question': question, 'return_path': return_path, 'newpk': new_question.pk, 'pk': pk})

def add_answers(request):
    valid = request.GET['valid'] # Получаем строку с отметками ответов
    pk = request.GET['pk']
    newpk = request.GET['newpk']
    question = CheckedQuestion.objects.get(pk=newpk)
    qst = Question.objects.get(pk=pk)
    i = 0
    for answer in qst.answers.all():
        CheckedAnswer.objects.create(answer=answer, valid=valid[i], question=question)
        i += 1
    return redirect(reverse_lazy('poll:index'))

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