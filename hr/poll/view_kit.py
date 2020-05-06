from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import KitForm, KitEditForm
from .models import Poll, UserProfile, Question, Kit



class KitList(LoginRequiredMixin, DetailView):  
    model = Poll
    template_name = 'poll/poll/kit_list.html'
    context_object_name = "poll"
    

class KitCreate(LoginRequiredMixin, CreateView, SingleObjectMixin):
    template_name = 'poll/kit/kit_create.html'
    form_class = KitForm

    def get_initial(self, *args, **kwargs):
        initial = super(KitCreate, self).get_initial(**kwargs)
        initial['poll'] = Poll.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('poll:poll_kit_list', kwargs={'pk': self.kwargs['pk']})


class KitDelete(LoginRequiredMixin, DeleteView):
    template_name = 'poll/kit/kit_delete.html'
    model = Kit

    def get_success_url(self):
        return reverse_lazy('poll:poll_kit_list', kwargs={'pk': self.object.poll.pk})

class KitEdit(LoginRequiredMixin, UpdateView):
    template_name = 'poll/kit/kit_edit.html'
    model = Kit
    form_class = KitEditForm
    
    def get_success_url(self):
        return reverse_lazy('poll:poll_kit_list', kwargs={'pk': self.object.poll.pk})
