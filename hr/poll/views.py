from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy

from .forms import ProfileCreationForm

"""
"""

def index(request):  
    context = {}  
    return render(request, 'poll/index.html', context) 


class RegisterView(FormView):
    """
    Создание пользователя
    """
    form_class = UserCreationForm

    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(RegisterView, self).form_valid(form)  


class CreateUserProfile(FormView):  
    """
    Создание профиля пользователя
    """
    form_class = ProfileCreationForm
    template_name = 'poll/profile_create.html'
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