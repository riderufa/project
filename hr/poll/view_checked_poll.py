from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# import redis
# import pickle

from .forms import PollForm, PollSetForm, KitForm
from .models import CheckedPoll, UserProfile, Question

# cache = redis.Redis(host='127.0.0.1', port=6379)

class CheckedPollList(SuccessMessageMixin, LoginRequiredMixin, ListView):  
    model = CheckedPoll
    template_name = 'poll/checked_poll/checked_poll_list.html'
    context_object_name = "polls"
    # login_url = 'login'
    # messages.add_message(request, messages.SUCCESS, 'jhgfjhfjhgfjhgf')
    success_message = 'asdfasdfasd'

    def get_queryset(self):
        current_user = UserProfile.objects.filter(user=self.request.user).first()
        # if current_user and current_user.type_user == 2:
            # cache.set(f'poll{new_poll.pk}user{request.user.pk}', pickle.dumps(new_poll.pk))
        return CheckedPoll.objects.filter(user__user=self.request.user, checked=True)
        # return Poll.objects.all()


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
