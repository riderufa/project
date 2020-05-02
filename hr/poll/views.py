from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import ProfileCreationForm, QuestionForm, PollForm
from .models import *

# Create your views here.

def index(request):  
    context = {}  
    return render(request, 'poll/index.html', context) 


class QuestionList(ListView):  
    model = Question
    template_name = 'question_list.html'
    context_object_name = "questions"

class QuestionDetailsView(DetailView):
    model = Question
    template_name = "poll/question_details.html"

class QuestionCreate(LoginRequiredMixin, CreateView):
    template_name = 'poll/question_create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('poll:question_list')
    login_url = 'login'

class QuestionEdit(LoginRequiredMixin, UpdateView):
    template_name = 'poll/question_edit.html'
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('poll:question_list')
    login_url = 'login'

class QuestionDelete(LoginRequiredMixin, DeleteView):
    template_name = 'poll/question_delete.html'
    model = Question
    success_url = reverse_lazy('poll:question_list')
    login_url = 'login'

class PollList(ListView):  
    model = Poll
    template_name = 'poll_list.html'
    context_object_name = "polls"

class PollDetailsView(DetailView):
    model = Poll
    template_name = "poll/poll_details.html"

class PollCreate(LoginRequiredMixin, CreateView):
    template_name = 'poll/poll_create.html'
    form_class = PollForm
    success_url = reverse_lazy('poll:index')
    login_url = 'login'


class PollEdit(LoginRequiredMixin, UpdateView):
    template_name = 'poll/poll_edit.html'
    model = Poll
    form_class = PollForm
    success_url = reverse_lazy('poll:index')
    login_url = 'login'

class PollDelete(LoginRequiredMixin, DeleteView):
    template_name = 'poll/poll_delete.html'
    model = Poll
    success_url = reverse_lazy('poll:index')
    login_url = 'login'


class RegisterView(FormView):

    form_class = UserCreationForm

    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(RegisterView, self).form_valid(form)  


class CreateUserProfile(FormView):  
  
    form_class = ProfileCreationForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('poll:index')

    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('poll:index'))  
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)  
  
    def form_valid(self, form):  
        instance = form.save(commit=False)  
        instance.user = self.request.user  
        instance.save()  
        return super(CreateUserProfile, self).form_valid(form)