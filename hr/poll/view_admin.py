from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
# from django.contrib.messages.views import SuccessMessageMixin


from .forms import PollForm, PollSetForm, KitForm
from .models import Poll, UserProfile, Question


"""
Контроллеры администратора
"""

class UserList(LoginRequiredMixin, ListView): 
    """
    Список пользователей
    """ 
    model = UserProfile
    template_name = 'poll/admin/user_list.html'
    context_object_name = "users"
    queryset = UserProfile.objects.filter(type_user=2) # Фильтрация по типу пользователя
 

class QuestionUserList(LoginRequiredMixin, ListView):  
    """
    Список пользователей конкретного вопроса
    """
    model = UserProfile
    template_name = 'poll/admin/user_list.html'
    context_object_name = "users"
    
    def get_queryset(self):
        return UserProfile.objects.filter(user_checked_polls__poll__questions__pk=self.kwargs['pk']) # Фильтрация


# class QuestionPollList(SuccessMessageMixin, LoginRequiredMixin, ListView):  
class QuestionPollList(LoginRequiredMixin, ListView):  
    """
    Список опросов конкретного вопроса
    """
    model = Poll
    template_name = 'poll/poll/poll_list.html'
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(questions__pk=self.kwargs['pk']).prefetch_related('user') #


class PollUserList(LoginRequiredMixin, ListView):  
    """
    Список пользователей конкретного опроса
    """
    model = UserProfile
    template_name = 'poll/admin/user_list.html'
    context_object_name = "users"

    def get_queryset(self):
        return UserProfile.objects.filter(user_checked_polls__poll__pk=self.kwargs['pk']) #


# class PollQuestionList(SuccessMessageMixin, LoginRequiredMixin, ListView):  
class PollQuestionList(LoginRequiredMixin, ListView):  
    """
    Список вопросов конкретного опроса
    """
    model = Question
    template_name = 'poll/question/question_list.html'
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.filter(checked_questions__poll__poll__pk=self.kwargs['pk']) #


# class UserPollList(SuccessMessageMixin, LoginRequiredMixin, ListView):  
class UserPollList(LoginRequiredMixin, ListView):  
    """
    Список опросов конкретного пользователя
    """
    model = Poll
    template_name = 'poll/poll/poll_list.html'
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(checked_poll__user__pk=self.kwargs['pk']).prefetch_related('user') #


# class UserQuestionList(SuccessMessageMixin, LoginRequiredMixin, ListView):  
class UserQuestionList(LoginRequiredMixin, ListView):  
    """
    Список вопросов конкретного пользователя
    """
    model = Question
    template_name = 'poll/question/question_list.html'
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.filter(checked_questions__poll__user__pk=self.kwargs['pk']) #

