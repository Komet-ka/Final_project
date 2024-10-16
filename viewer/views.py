from datetime import timedelta

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

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

LOGGER = getLogger()

from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm


class EventsView(TemplateView):
    template_name = 'events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Získání aktuálního data
        today = timezone.now().date()
        one_year_ago = today - timedelta(days=365)

        # Načtení schválených událostí
        events = Event.objects.filter(is_approved=True)
        event_type_filter = self.request.GET.get("event_type", "")
        if event_type_filter:
            events = events.filter(eventType__id=int(event_type_filter))

        # Rozdělení na proběhlé a aktuální události
        past_events = events.filter(date__lt=today, date__gte=one_year_ago)
        upcoming_events = events.filter(date__gte=today)

        # Stránkování jen s aktuálními událostmi
        paginator = Paginator(upcoming_events, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pokud je na stránce méně než 6 aktuálních událostí, doplň je dalšími
        if len(page_obj) < 6:
            remaining_count = 6 - len(page_obj)
            additional_events = upcoming_events.exclude(id__in=[event.id for event in page_obj])[:remaining_count]
            page_obj.object_list = list(page_obj.object_list) + list(additional_events)

        context['page_obj'] = page_obj
        context['past_events'] = past_events

        return context

class EventFilterView(TemplateView):
    template_name = 'type_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Získání aktuálního data a data před rokem
        today = timezone.now().date()
        one_year_ago = today - timedelta(days=365)

        # Filtrovat události podle eventType a 'pk'
        events = Event.objects.filter(eventType=kwargs.get('pk'), is_approved=True)

        # Rozdělení na proběhlé a aktuální události
        past_events = events.filter(date__lt=today, date__gte=one_year_ago)
        upcoming_events = events.filter(date__gte=today)

        # Stránkování jen s aktuálními událostmi
        paginator = Paginator(upcoming_events, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pokud je na stránce méně než 6 aktuálních událostí, doplň je dalšími
        if len(page_obj) < 6:
            remaining_count = 6 - len(page_obj)
            additional_events = upcoming_events.exclude(id__in=[event.id for event in page_obj])[:remaining_count]
            page_obj.object_list = list(page_obj.object_list) + list(additional_events)

        context['page_obj'] = page_obj
        context['past_events'] = past_events

        return context

class MyEventsView(TemplateView):
    template_name = 'my_attendees.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Získání aktuálního data a data před rokem
        today = timezone.now().date()
        one_year_ago = today - timedelta(days=365)

        # Filtrovat události podle přihlášeného uživatele (události, na které se přihlásil)
        events = Event.objects.filter(attendees=self.request.user, is_approved=True)
        # Filtrovat události podle uživatele, který událost vytvořil
        my_events = Event.objects.filter(user=self.request.user, is_approved=True)

        # Stránkování - 6 událostí na stránku
        paginator = Paginator(events, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Stránkování - 6 událostí na stránku pro moje události
        paginator_my = Paginator(my_events, 6)
        page_number_my = self.request.GET.get('page_my')  # Přidáme jiný parametr pro stránkování
        page_my_obj = paginator_my.get_page(page_number_my)

        # Přidat stránkované objekty do kontextu
        context['page_obj'] = page_obj  # Události, na které se přihlásil uživatel
        context['page_my_obj'] = page_my_obj  # Události, které vytvořil uživatel

        context['today'] = today  # Přidání aktuálního data do kontextu
        context['one_year_ago'] = one_year_ago  # Přidání data před rokem do kontextu

        return context


class EventCreateView(PermissionRequiredMixin, CreateView):

  template_name = 'event_update_create_form.html'
  form_class = EventForm
  success_url = reverse_lazy('events')
  permission_required = 'viewer.add_event'

  def form_valid(self, form):
    form.instance.user = self.request.user  # Nastav aktuálně přihlášeného uživatele
    return super().form_valid(form)
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

  def delete(self, request, *args, **kwargs):
      self.object = self.get_object()

      # Odstranit všechny vazby účastníků
      self.object.attendees.clear()  # Odstraní všechny účastníky

      # Pokud máš další související záznamy, jako např. komentáře, které se vztahují na událost,
      # musíš je také odstranit. Např.:
      # self.object.comments.all().delete()  # (přizpůsob si podle svého modelu)

      # Nyní můžeš událost smazat
      self.object.delete()
      return HttpResponseRedirect(self.get_success_url())

class EventTypeView(ListView):
  template_name = 'administrace.html'
  model = EventType
  ordering = ['name']

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # Filtrovat události podle schválení
    events = Event.objects.filter(is_approved=False)
    event_types = EventType.objects.filter(is_approved=False)

    context['events'] = events  # Přidání událostí do kontextu
    context['event_types'] = event_types  # Přidání událostí do kontextu

    return context

  def post(self, request, *args, **kwargs):
    # Zpracování událostí
    if 'event_ids' in request.POST:
        event_ids = request.POST.getlist('event_ids')  # Získání seznamu ID událostí
        for event_id in event_ids:
            event = Event.objects.get(pk=event_id)
            is_approved = f'is_approved' in request.POST and event_id in request.POST.getlist('is_approved')  # Zjistit, zda je zaškrtnuté
            event.is_approved = is_approved
            event.save()

    # Zpracování typů událostí
    if 'type_ids' in request.POST:
        type_ids = request.POST.getlist('type_ids')  # Získání seznamu ID typů
        for type_id in type_ids:
            event_type = EventType.objects.get(pk=type_id)
            is_approved = f'type_approved' in request.POST and type_id in request.POST.getlist('type_approved')  # Zjistit, zda je zaškrtnuté
            event_type.is_approved = is_approved
            event_type.save()

    return redirect('administrace')  # Přesměrování zpět na stránku


class EventTypeCreateView(PermissionRequiredMixin, CreateView):
  template_name = 'form.html'
  form_class = EventTypeForm
  success_url = reverse_lazy('administrace')
  permission_required = 'viewer.add_eventtype'

  def form_invalid(self, form):
      LOGGER.warning(f'User provided invalid data. {form.errors}')
      return super().form_invalid(form)

class EventTypeUpdateView(PermissionRequiredMixin, UpdateView):
  template_name = 'form.html'
  model = EventType
  form_class = EventTypeForm
  success_url = reverse_lazy('administrace')
  permission_required = 'viewer.add_eventtype'

  def form_invalid(self, form):
      LOGGER.warning('User provided invalid data while updating a movie.')
      return super().form_invalid(form)


class EventTypeDeleteView(PermissionRequiredMixin, DeleteView):
  template_name = 'type_confirm_delete.html'
  model = EventType
  success_url = reverse_lazy('administrace')
  permission_required = 'viewer.add_eventtype'


def detail(request, pk):
  event = get_object_or_404(Event, pk=pk)
  user_is_attendee = event.attendees.filter(id=request.user.id).exists() if request.user.is_authenticated else False
  if event.is_capacity_limited and event.capacity is not None:
      remaining_capacity = event.capacity - event.attendees.count()
  else:
      remaining_capacity = None

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
             'attendees': event.attendees.all(),
             'user_is_attendee': user_is_attendee,
             'attendee_count': event.attendees.count(),
             'remaining_capacity': remaining_capacity,
             }
  )


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user:  # Zkontroluj, zda je aktuální uživatel autorem komentáře
        comment.delete()  # Smaž komentář
    return redirect('detail', pk=comment.event.pk)  # Přesměruj na detail události

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
          "nearest_events": Event.objects.order_by("date").all()[:5],
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
        # Zkontroluj, zda je uživatel již účastníkem
        if user in event.attendees.all():
            event.attendees.remove(user)  # Odhlásit uživatele
            messages.success(request, f"Úspěšně jste se odhlásili z akce {event.name}.")
        else:
            # Zkontroluj, zda je kapacita omezena a zda je plná
            if event.is_capacity_limited and event.attendees.count() >= event.capacity:
                messages.error(request, "Nelze se přihlásit, kapacita je plná.")
            else:
                event.attendees.add(user)  # Přihlásit uživatele
                messages.success(request, f"Úspěšně jste se přihlásili na akci {event.name}.")

        return redirect('detail', pk=event.pk)

    # Pokud je metoda GET, odhlásit uživatele nebo přihlásit
    if user in event.attendees.all():
        event.attendees.remove(user)  # Odhlásit uživatele
        messages.success(request, f"Úspěšně jste se odhlásili z akce {event.name}.")
    else:
        # Zkontroluj, zda je kapacita omezena a zda je plná
        if event.is_capacity_limited and event.attendees.count() >= event.capacity:
            messages.error(request, "Nelze se přihlásit, kapacita je plná.")
        else:
            event.attendees.add(user)  # Přihlásit uživatele
            messages.success(request, f"Úspěšně jste se přihlásili na akci {event.name}.")

    return redirect('my_attendees')


class LoginView(auth_views.LoginView):
  form_class = CustomAuthenticationForm


def search_view(request):
    form = SearchForm(request.GET or None)
    results = []

    if form.is_valid():
        results = form.search()

    return render(request, 'search.html', {'results': results})


def global_data(request):
    data = EventType.objects.filter(is_approved=True)
    return {'type_list': data}


def custom_403_view(request, exception):
  return render(request, '403.html', status=403)

  def my_view(request):
    if not request.user.has_perm('viewer.add_eventtype'):
      raise PermissionDenied("Nemáte oprávnění k provedení této akce.")



def api_upcoming_events(request):
    upcoming_events = Event.objects.filter(date__gt=timezone.now())
    json_upcoming_events = {}
    for event in upcoming_events:
        json_upcoming_events[event.pk] = {
            "Název": event.name,
            "Datum": event.date
        }
    return JsonResponse(json_upcoming_events)
def list_events(request):
    import requests
    responce = requests.get("http://127.0.0.1:8000/api/get/all_events/")
    události = responce.json()
    return render(request, "api_list_events.html", context={"events": události})
















