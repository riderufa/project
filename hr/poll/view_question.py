from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import QuestionForm
from .models import Question

"""
Контроллеры вопроса
"""

class QuestionList(LoginRequiredMixin, ListView):  
    """
    Список вопросов
    """
    model = Question
    template_name = 'poll/question/question_list.html'
    context_object_name = "questions"


class QuestionDetail(LoginRequiredMixin, DetailView):
    """
    Подробная информация о вопросе
    """
    model = Question
    template_name = "poll/question/question_details.html"
    queryset = Question.objects.all().prefetch_related('answers')


class QuestionCreate(LoginRequiredMixin, CreateView):
    """
    Создание вопроса
    """
    template_name = 'poll/question/question_create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('poll:question_list')


class QuestionEdit(LoginRequiredMixin, UpdateView):
    """
    Редактирование вопроса
    """
    template_name = 'poll/question/question_edit.html'
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('poll:question_list')

    # Проверяем, чтобы количество верных ответов соответствовало типу вопроса
    def form_valid(self, form):
        question = Question.objects.get(pk=self.kwargs['pk'])
        if form.instance.type == 1:
            answer_valid = 0
            for answer in question.answers.all():
                if answer.valid:
                    answer_valid += 1
            if answer_valid > 1:
                response = super().form_invalid(form)
                messages.add_message(self.request, messages.INFO, 'В вопросе типа mono не может быть более одного верного ответа.', extra_tags='alert-danger')
                return response
        return super(QuestionEdit, self).form_valid(form)


class QuestionDelete(LoginRequiredMixin, DeleteView):
    """
    Удаление вопроса
    """
    template_name = 'poll/question/question_delete.html'
    model = Question
    success_url = reverse_lazy('poll:question_list')
