from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from viewer.models import Event, EventType, User, Comment
import re
from django.forms.widgets import Textarea, DateInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Uživatelské jméno')
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput)

class EventForm(ModelForm):

  class Meta:
    model = Event
    exclude = ['attendees']

  #title = CharField(validators=[capitalized_validator])
  #rating = IntegerField(min_value=1, max_value=10)
  #released = PastMonthField()

  def clean_description(self):
    # Každá věta bude začínat velkým písmenem
    initial = self.cleaned_data['description']
    sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
    return '. '.join(sentence.capitalize() for sentence in sentences)

class EventTypeForm(ModelForm):
  class Meta:
    model = EventType
    fields = '__all__'
    labels = {'name': 'Název',
            }

class SignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = ['username', 'first_name', 'last_name']
    labels = {'username': 'Uživatelské jméno',
              'first_name': 'Jméno',
              'last_name': 'Příjmení',
              }
  def save(self, commit=True):
    self.instance.is_active = True
    return super().save(commit)


class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    labels = {'username': 'Uživatelské jméno',
              'first_name': 'Jméno',
              'last_name': 'Příjmení',
              'email': 'email',
              }

class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'describtion', 'eventType', 'date', 'place', 'entry']
    labels = {'name': 'Název',
              'describtion': 'Popis',
              'eventType': 'Typ akce',
              'date': 'Datum',
              'place': 'Místo',
              'entry': 'Vstupné',
              }
    widgets = {
        'describtion': Textarea(attrs={'rows': 5, 'cols': 40}),
        'date': DateInput(attrs={'type': 'date'})  # Kalendář pro výběr data
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Přidání skrytého pole pro uživatele
        self.fields['user'] = forms.HiddenInput()  # Skryté pole pro 'user'

class SearchForm(forms.Form):
    query = forms.CharField(
        label='',  # Schováme label
        widget=forms.TextInput(
            attrs={
                'class': 'form-control me-2',  # Třídy Bootstrapu
                'placeholder': 'Hledat',  # Placeholder pro vyhledávací pole
                'aria-label': 'Search'  # Atribut pro přístupnost
            }
        )
    )

    def search(self):
        query = self.cleaned_data.get('query')
        # Příklad vyhledávání v několika modelech
        results = []
        if query:
            # Procházení modelů a hledání podle zadaného dotazu
            results += Comment.objects.filter(comment__icontains=query)
            results += Event.objects.filter(
                Q(name__icontains=query) | Q(place__icontains=query) |
                Q(describtion__icontains=query) | Q(date__icontains=query)
            )
        return results