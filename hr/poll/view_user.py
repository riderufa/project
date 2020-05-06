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
    
    poll = Poll.objects.get(pk=pk)
    user = UserProfile.objects.get(user=request.user)
    if CheckedPoll.objects.filter(poll=poll, user=user).first():
        new_poll = CheckedPoll.objects.get(poll=poll, user=user)
    else:
        new_poll = CheckedPoll.objects.create(poll=poll, user=user)
    
    poll_pk = cache.get(f'poll{new_poll.pk}user{request.user.pk}')
    if not poll_pk:
        cache.set(f'poll{new_poll.pk}user{request.user.pk}', pickle.dumps(new_poll.pk))
        cache.set(f'user{request.user.pk}', pickle.dumps(new_poll.pk)) # , ex=poll.time_limit

    elif not cache.get(f'user{request.user.pk}'):
        return redirect(reverse_lazy('poll:index'))

    questions = Question.objects.filter(polls__pk=pk)
    return render(request, 'poll/user/user_question_list.html', context={'questions': questions})


def question_get_answer(request, pk):
    
    poll_pk = pickle.loads(cache.get(f'user{request.user.pk}'))
    # print(poll_pk)
    # poll_id = cache.get('adverts')
    # if adverts:
    #     adverts_value = pickle.loads(adverts)
    # else:
    #     adverts_value = Advert.objects.all()
    #     cache.set(f`poll{pk}user`, pickle.dumps(adverts_value))

    question = Question.objects.get(pk=pk)
    poll = CheckedPoll.objects.get(pk=poll_pk)
    if CheckedQuestion.objects.filter(poll=poll, question=question).first():
        new_question = CheckedQuestion.objects.get(poll=poll, question=question)
    else:
        new_question = CheckedQuestion.objects.create(question=question, poll=poll)
    
    # question_pk = cache.get(f'question{new_question.pk}user{request.user.pk}')
    # if not poll_pk:
    #     cache.set(f'poll{new_poll.pk}user{request.user.pk}', pickle.dumps(new_poll.pk))
    #     cache.set(f'user{request.user.pk}', pickle.dumps(new_poll.pk)) # , ex=poll.time_limit

    # elif not cache.get(f'user{request.user.pk}'):
    #     return redirect(reverse_lazy('poll:index'))
    
    return_path  = request.META.get('HTTP_REFERER','/')
    question = Question.objects.get(pk=pk)
    return render(request, 'poll/user/question_get_answer.html', context={'question': question, 'return_path': return_path})

def question_save_answer(request, pk):
    pass    

def question_get_answer1(request, pk):

    question = Question.objects.get(pk=pk)
    answers = question.answers.all()
    l = answers.count()
    print(l)
    AnswerFormSet = modelformset_factory(CheckedAnswer, form=CheckedAnswerForm, extra=l)

    if request.method == 'POST':
        formset = AnswerFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('poll:index')
    else:
        formset = AnswerFormSet()
    context = {'formset': formset, 'answers': answers}
    return render(request, 'poll/user/question_get_answer1.html', context)