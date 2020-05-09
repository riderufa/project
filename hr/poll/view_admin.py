from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


from .forms import PollForm, PollSetForm, KitForm
from .models import Poll, UserProfile, Question


class UserList(LoginRequiredMixin, ListView):  
    model = UserProfile
    template_name = 'poll/admin/user_list.html'
    context_object_name = "users"
    queryset = UserProfile.objects.filter(type_user=2)
    # login_url = 'login'

    # def get_queryset(self):
    #     current_user = UserProfile.objects.filter(user=self.request.user).first()
    #     if current_user and current_user.type_user == 2:
    #         return Poll.objects.filter(user__user=self.request.user)
    #     return Poll.objects.all()

class QuestionUserList(LoginRequiredMixin, ListView):  
    model = UserProfile
    template_name = 'poll/admin/user_list.html'
    context_object_name = "users"
    # queryset = UserProfile.objects.filter(pk=pk)
    # login_url = 'login'

    def get_queryset(self):
        # current_user = UserProfile.objects.filter(user=self.request.user).first()
        # if current_user and current_user.type_user == 2:
        #     return Poll.objects.filter(user__user=self.request.user)
        return UserProfile.objects.filter(user_checked_polls__poll__questions__pk=self.kwargs['pk'])

class QuestionPollList(SuccessMessageMixin, LoginRequiredMixin, ListView):  
    model = Poll
    template_name = 'poll/poll/poll_list.html'
    context_object_name = "polls"
    login_url = 'login'

    def get_queryset(self):
        # current_user = UserProfile.objects.filter(user=self.request.user).first()
        # if current_user and current_user.type_user == 2:
        #     return Poll.objects.filter(user__user=self.request.user)
        return Poll.objects.filter(questions__pk=self.kwargs['pk'])

# class PollDetail(LoginRequiredMixin, DetailView):
#     model = Poll
#     template_name = "poll/poll/poll_details.html"
#     login_url = 'login'


# class PollCreate(LoginRequiredMixin, CreateView):
#     template_name = 'poll/poll/poll_create.html'
#     form_class = PollForm
#     success_url = reverse_lazy('poll:index')
#     login_url = 'login'

#     def get_initial(self, *args, **kwargs):
#         initial = super(PollCreate, self).get_initial(**kwargs)
#         initial['admin'] = UserProfile.objects.get(user=self.request.user)
#         return initial


# class PollEdit(LoginRequiredMixin, UpdateView):
#     template_name = 'poll/poll/poll_edit.html'
#     model = Poll
#     form_class = PollForm
#     success_url = reverse_lazy('poll:index')
#     login_url = 'login'


# class PollSet(LoginRequiredMixin, UpdateView):
#     template_name = 'poll/poll/poll_edit.html'
#     model = Poll
#     form_class = PollSetForm
#     success_url = reverse_lazy('poll:index')
#     login_url = 'login'


# class PollDelete(LoginRequiredMixin, DeleteView):
#     template_name = 'poll/poll/poll_delete.html'
#     model = Poll
#     success_url = reverse_lazy('poll:index')
#     login_url = 'login'
