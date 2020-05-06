from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import QuestionForm
from .models import Question


class QuestionList(LoginRequiredMixin, ListView):  
    model = Question
    template_name = 'poll/question/question_list.html'
    context_object_name = "questions"

class QuestionDetail(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "poll/question/question_details.html"

class QuestionCreate(LoginRequiredMixin, CreateView):
    template_name = 'poll/question/question_create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('poll:question_list')

class QuestionEdit(LoginRequiredMixin, UpdateView):
    template_name = 'poll/question/question_edit.html'
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('poll:question_list')

class QuestionDelete(LoginRequiredMixin, DeleteView):
    template_name = 'poll/question/question_delete.html'
    model = Question
    success_url = reverse_lazy('poll:question_list')
