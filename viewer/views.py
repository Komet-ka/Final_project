from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from logging import getLogger

from viewer.forms import EventForm, EventTypeForm
from viewer.models import Event, EventType, Comment

LOGGER = getLogger()

class EventsView(TemplateView):
  template_name = 'main_page.html'
  extra_context = {'events': Event.objects.all()}

class EventCreateView(PermissionRequiredMixin, CreateView):

  template_name = 'form.html'
  form_class = EventForm
  success_url = reverse_lazy('main_page')
  permission_required = 'viewer.add_event'

  def form_invalid(self, form):
    LOGGER.warning(f'User provided invalid data. {form.errors}')
    return super().form_invalid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'form.html'
  model = Event
  form_class = EventForm
  success_url = reverse_lazy('main_page')

  def form_invalid(self, form):
      LOGGER.warning('User provided invalid data while updating a movie.')
      return super().form_invalid(form)

class EventDeleteView(DeleteView):
  template_name = 'event_confirm_delete.html'
  model = Event
  success_url = reverse_lazy('main_page')


class EventTypeView(ListView):
  template_name = 'types.html'
  model = EventType


class EventTypeCreateView(LoginRequiredMixin, CreateView):
  template_name = 'form.html'
  form_class = EventTypeForm
  success_url = reverse_lazy('types')

  def form_invalid(self, form):
      LOGGER.warning(f'User provided invalid data. {form.errors}')
      return super().form_invalid(form)

class EventTypeUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'form.html'
  model = EventType
  form_class = EventTypeForm
  success_url = reverse_lazy('types')

  def form_invalid(self, form):
      LOGGER.warning('User provided invalid data while updating a movie.')
      return super().form_invalid(form)


class EventTypeDeleteView(LoginRequiredMixin, DeleteView):
  template_name = 'type_confirm_delete.html'
  model = EventType
  success_url = reverse_lazy('types')


def detail(request, event_pk):
  if "comment" in request.POST:
    new_comment = Comment()
    new_comment.uzivatel = request.POST.get("uzivatel", "")
    new_comment.comment = request.POST.get("komentar", "")
    new_comment.event = Event.objects.get(pk=event_pk)
    new_comment.save()
    pass

  return render(
    request, template_name='detail.html',
    context={'event': Event.objects.get(pk=event_pk),
             'coments': Comment.objects.filter(event__pk=event_pk)}
  )