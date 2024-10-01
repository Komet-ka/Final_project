from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from logging import getLogger

from viewer.forms import EventForm, EventTypeForm
from viewer.models import Event, EventType, Comment

LOGGER = getLogger()

class EventsView(TemplateView):
  template_name = 'events.html'
  extra_context = {'events': Event.objects.all()}

class EventCreateView(PermissionRequiredMixin, CreateView):

  template_name = 'form.html'
  form_class = EventForm
  success_url = reverse_lazy('events')
  permission_required = 'viewer.add_event'

  def form_invalid(self, form):
    LOGGER.warning(f'User provided invalid data. {form.errors}')
    return super().form_invalid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'form.html'
  model = Event
  form_class = EventForm
  success_url = reverse_lazy('events')

  def form_invalid(self, form):
      LOGGER.warning('User provided invalid data while updating a movie.')
      return super().form_invalid(form)

class EventDeleteView(LoginRequiredMixin, DeleteView):
  template_name = 'event_confirm_delete.html'
  model = Event
  success_url = reverse_lazy('events')


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


def detail(request, pk):
  if "comment" in request.POST:
    if request.user.is_authenticated:
      new_comment = Comment()
      new_comment.user = request.user  # Používáme aktuálního přihlášeného uživatele
      new_comment.comment = request.POST.get("comment", "")
      new_comment.event = get_object_or_404(Event, pk=pk)
      new_comment.save()
    else:
      # Pokud uživatel není přihlášen, můžeš vrátit nějakou chybovou hlášku nebo přesměrovat
      return redirect('login')

  return render(
    request, template_name='detail.html',
    context={'event': get_object_or_404(Event, pk=pk),
             'comments': Comment.objects.filter(event__pk=pk)}
  )