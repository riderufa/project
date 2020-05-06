from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import AnswerForm
from .models import Answer, Question


class AnswerList(LoginRequiredMixin, DetailView):  
    model = Question
    template_name = 'poll/answer/answer_list.html'
    context_object_name = "question"
    login_url = 'login'


class AnswerCreate(LoginRequiredMixin, CreateView, SingleObjectMixin):
    template_name = 'poll/answer/answer_create.html'
    form_class = AnswerForm
    success_url = reverse_lazy('poll:question_list')
    login_url = 'login'

    def get_initial(self, *args, **kwargs):
        initial = super(AnswerCreate, self).get_initial(**kwargs)
        initial['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return initial

 
class AnswerEdit(LoginRequiredMixin, UpdateView):
    template_name = 'poll/answer/answer_edit.html'
    model = Answer
    form_class = AnswerForm
    login_url = 'login'
    
    def get_success_url(self):
        return reverse_lazy('poll:answer_list', kwargs={'pk': self.object.question.pk})


class AnswerDelete(LoginRequiredMixin, DeleteView):
    template_name = 'poll/answer/answer_delete.html'
    model = Answer
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('poll:answer_list', kwargs={'pk': self.object.question.pk})
