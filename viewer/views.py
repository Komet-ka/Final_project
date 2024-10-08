from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from logging import getLogger

from viewer.forms import EventForm, EventTypeForm, SignUpForm, UserForm, SearchForm
from viewer.models import Event, EventType, Comment, User

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden


LOGGER = getLogger()

from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm


class EventsView(TemplateView):
  template_name = 'events.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    events = Event.objects.all()
    paginator = Paginator(events, 6)  # 6 událostí na stránku

    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['page_obj'] = page_obj
    return context

class EventFilterView(TemplateView):
  template_name = 'type_filter.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['events'] = Event.objects.filter(eventType=kwargs.get('pk'))
    return context

class EventCreateView(PermissionRequiredMixin, CreateView):

  template_name = 'event_update_create_form.html'
  form_class = EventForm
  success_url = reverse_lazy('events')
  permission_required = 'viewer.add_event'
  def form_invalid(self, form):
    LOGGER.warning(f'User provided invalid data. {form.errors}')
    return super().form_invalid(form)

class EventUpdateView(PermissionRequiredMixin, UpdateView):
  template_name = 'event_update_create_form.html'
  model = Event
  form_class = EventForm
  success_url = reverse_lazy('events')
  permission_required = 'viewer.add_event'

  def form_invalid(self, form):
      LOGGER.warning('User provided invalid data while updating a movie.')
      return super().form_invalid(form)

class EventDeleteView(PermissionRequiredMixin, DeleteView):
  template_name = 'event_confirm_delete.html'
  model = Event
  success_url = reverse_lazy('events')
  permission_required = 'viewer.add_event'

class EventTypeView(ListView):
  template_name = 'types.html'
  model = EventType


class EventTypeCreateView(PermissionRequiredMixin, CreateView):
  template_name = 'form.html'
  form_class = EventTypeForm
  success_url = reverse_lazy('types')
  permission_required = 'viewer.add_eventtype'

  def form_invalid(self, form):
      LOGGER.warning(f'User provided invalid data. {form.errors}')
      return super().form_invalid(form)

class EventTypeUpdateView(PermissionRequiredMixin, UpdateView):
  template_name = 'form.html'
  model = EventType
  form_class = EventTypeForm
  success_url = reverse_lazy('types')
  permission_required = 'viewer.add_eventtype'

  def form_invalid(self, form):
      LOGGER.warning('User provided invalid data while updating a movie.')
      return super().form_invalid(form)


class EventTypeDeleteView(PermissionRequiredMixin, DeleteView):
  template_name = 'type_confirm_delete.html'
  model = EventType
  success_url = reverse_lazy('types')
  permission_required = 'viewer.add_eventtype'


def detail(request, pk):
  event = get_object_or_404(Event, pk=pk)
  user_is_attendee = event.attendees.filter(id=request.user.id).exists() if request.user.is_authenticated else False

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
    context={'event': event,
             'comments': Comment.objects.filter(event__pk=pk),
             'user_is_attendee': user_is_attendee}
  )

def my_page(request):
    return render(
      request,
      "my_page.html",
      context={}
    )


def main_page(request):
  return render(
    request,
    "main_page.html",
    context={
          "newest_events": Event.objects.order_by("-create_date").all()[:5],
          "nearest_events": Event.objects.order_by("-date").all()[:5],
          "newest_comments": Comment.objects.order_by("-comment_date").all()[:5],
    }
  )

class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('my_page')


class UserUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'form.html'
  model = User
  form_class = UserForm
  success_url = reverse_lazy('my_page')

  def get_object(self):
    return self.request.user

  def form_invalid(self, form):
    LOGGER.warning('User provided invalid data while updating their profile.')
    return super().form_invalid(form)

class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'


def logout_view(request):
  logout(request)
  messages.success(request, 'Úspěšně jste se odhlásili.')
  return redirect('main_page')

def attendees(request, pk):
  event = get_object_or_404(Event, pk=pk)
  user = request.user

  if request.method == "POST":
    if user in event.attendees.all():  # Zkontroluj, zda je uživatel již účastníkem
      event.attendees.remove(user)  # Odhlásit uživatele
      messages.success(request, f"Úspěšně jste se odhlásili z akce {event.name}.")
    else:
      event.attendees.add(user)  # Přihlásit uživatele
      messages.success(request, f"Úspěšně jste se přihlásili na akci {event.name}.")

    return redirect('detail', pk=event.pk)
  else:
    if user in event.attendees.all():  # Zkontroluj, zda je uživatel již účastníkem
      event.attendees.remove(user)  # Odhlásit uživatele
      messages.success(request, f"Úspěšně jste se odhlásili z akce {event.name}.")
    else:
      event.attendees.add(user)  # Přihlásit uživatele
      messages.success(request, f"Úspěšně jste se přihlásili na akci {event.name}.")

    return redirect('my_attendees')



class MyEventsView(TemplateView):
  template_name = 'my_attendees.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Filtrovat události podle přihlášeného uživatele
    context['events'] = Event.objects.filter(attendees=self.request.user)
    return context

class LoginView(auth_views.LoginView):
  form_class = CustomAuthenticationForm


def search_view(request):
    form = SearchForm(request.GET or None)
    results = []

    if form.is_valid():
        results = form.search()

    return render(request, 'search.html', {'results': results})


def global_data(request):
    data = EventType.objects.all()
    return {'type_list': data}


def custom_403_view(request, exception):
  return render(request, '403.html', status=403)

  def my_view(request):
    if not request.user.has_perm('viewer.add_eventtype'):
      raise PermissionDenied("Nemáte oprávnění k provedení této akce.")