from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models.signals import post_save

from .forms import KitForm, KitEditForm
from .models import Poll, UserProfile, Question, Kit, CheckedPoll

def post_save_kit(sender, **kwargs):
    poll = Poll.objects.get(pk=kwargs['instance'].poll.pk)
    if kwargs['created']:
        if poll.rank:
            poll.rank = poll.rank + kwargs['instance'].rank
        else:
            poll.rank = kwargs['instance'].rank
        poll.save()

post_save.connect(post_save_kit, sender=Kit)

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
        return reverse_lazy('poll:kit_list', kwargs={'pk': self.kwargs['pk']})

    # def form_valid(self, form_class):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     form_class.send_email()
    #     return super(KitView, self).form_valid(form_class)

    # def form_valid(self, form_class):
    #     kit = super(KitCreate, self).form_valid(form_class)
    #     print(kit)
    #     poll = CheckedPoll.objects.get(pk=kit.instance.pk)
    #     poll.rank += kit.rank
    #     poll.save()
    #     form.instance.created_by = self.request.user
    #     return kit


class KitDelete(LoginRequiredMixin, DeleteView):
    template_name = 'poll/kit/kit_delete.html'
    model = Kit

    def get_success_url(self):
        return reverse_lazy('poll:kit_list', kwargs={'pk': self.object.poll.pk})

class KitEdit(LoginRequiredMixin, UpdateView):
    template_name = 'poll/kit/kit_edit.html'
    model = Kit
    form_class = KitEditForm
    
    def get_success_url(self):
        return reverse_lazy('poll:kit_list', kwargs={'pk': self.object.poll.pk})
