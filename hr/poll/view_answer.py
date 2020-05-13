from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib import messages

from .forms import AnswerForm
from .models import Answer, Question

"""
Контроллеры ответов
"""

class AnswerList(LoginRequiredMixin, DetailView):  
    """
    Список ответов
    """
    model = Question
    template_name = 'poll/answer/answer_list.html'
    context_object_name = "question"
    queryset = Question.objects.all().prefetch_related('answers')


class AnswerCreate(LoginRequiredMixin, CreateView, SingleObjectMixin):
    """
    Создание ответа
    """
    model = Answer
    template_name = 'poll/answer/answer_create.html'
    form_class = AnswerForm
    success_url = reverse_lazy('poll:question_list')

    # Добавляем при инициализации конкретный вопрос в форму
    def get_initial(self, *args, **kwargs):
        initial = super(AnswerCreate, self).get_initial(**kwargs)
        initial['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return initial

    # Проверяем, чтобы количество верных ответов соответствовало типу вопроса
    def form_valid(self, form):
        question = Question.objects.get(pk=self.kwargs['pk']) # Извлекаем pk вопроса с помощью SingleObjectMixin
        if form.instance.valid and question.type == 1:
            for answer in question.answers.all():
                if answer.valid:
                    response = super().form_invalid(form)
                    messages.add_message(self.request, messages.INFO, 'В вопросе типа mono не может быть более одного верного ответа.', extra_tags='alert-danger')
                    return response
        return super(AnswerCreate, self).form_valid(form)

 
class AnswerEdit(LoginRequiredMixin, UpdateView):
    """
    Редактирование ответа
    """
    template_name = 'poll/answer/answer_edit.html'
    model = Answer
    form_class = AnswerForm
    
    def get_success_url(self):
        return reverse_lazy('poll:answer_list', kwargs={'pk': self.object.question.pk})

    # Проверяем, чтобы количество верных ответов соответствовало типу вопроса
    def form_valid(self, form):
        answer = Answer.objects.get(pk=self.kwargs['pk'])
        question = Question.objects.get(pk=answer.question.pk)
        if form.instance.valid and question.type == 1:
            for answer in question.answers.all():
                if answer.valid:
                    response = super().form_invalid(form)
                    messages.add_message(self.request, messages.INFO, 'В вопросе типа mono не может быть более одного верного ответа.', extra_tags='alert-danger')
                    return response
        return super(AnswerEdit, self).form_valid(form)


class AnswerDelete(LoginRequiredMixin, DeleteView):
    """
    Удаление ответа
    """
    template_name = 'poll/answer/answer_delete.html'
    model = Answer

    def get_success_url(self):
        return reverse_lazy('poll:answer_list', kwargs={'pk': self.object.question.pk})
