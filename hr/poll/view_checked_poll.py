from django.shortcuts import render
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView
# from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy
# from django.contrib import messages

import redis
import pickle

# from .forms import PollForm, PollSetForm, KitForm
# from .models import CheckedPoll, UserProfile, Question
from .models import CheckedPoll, UserProfile
# from .view_stat import answer_stat

"""
Контроллеры пройденных опросов
"""

cache = redis.Redis(host='REDIS_URL', port=6379)


class UserCheckedPollList(LoginRequiredMixin, ListView):  
    """
    Список пройденных опросов текущего пользователя
    """
    model = CheckedPoll
    template_name = 'poll/checked_poll/user_checked_poll_list.html'
    context_object_name = "polls"

    def get_queryset(self):
        current_user = UserProfile.objects.filter(user=self.request.user).first()
        return CheckedPoll.objects.filter(user__user=self.request.user, checked=True).select_related('poll').prefetch_related('questions').prefetch_related('questions__answers').prefetch_related('questions__answers__answer')


    # Добавляем в контекст данные из редис для контроля времени
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll_pk = cache.get(f'pu{self.request.user.pk}')
        ttl_poll = 0
        if poll_pk:
            ttl_poll = cache.ttl(f'p{pickle.loads(poll_pk)}u{self.request.user.pk}time')
            context['new_poll_pk'] = pickle.loads(poll_pk)
        context['ttl_poll'] = ttl_poll
        
        return context


class AdminCheckedPollList(LoginRequiredMixin, ListView):  
    """
    Список пройденных опросов
    """
    model = CheckedPoll
    template_name = 'poll/checked_poll/admin_checked_poll_list.html'
    context_object_name = "polls"

    def get_queryset(self):
        return CheckedPoll.objects.filter(checked=True).select_related('poll').prefetch_related('questions').prefetch_related('questions__answers').prefetch_related('questions__answers__answer')

