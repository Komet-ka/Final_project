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
    new_event_type = forms.CharField(
        max_length=100,
        required=False,
        label="Vytvořit nový typ události a odeslat ke schválení"
    )

    class Meta:
        model = Event
        fields = ['name', 'describtion', 'eventType', 'date', 'place', 'link', 'entry', 'image', 'is_capacity_limited', 'capacity', 'new_event_type']
        labels = {
            'name': 'Název',
            'describtion': 'Popis',
            'eventType': 'Typ akce',
            'date': 'Datum',
            'place': 'Místo',
            'link': 'Odkaz',
            'entry': 'Vstupné',
            'image': 'Obrázek',
        }

        widgets = {
            'describtion': Textarea(attrs={'rows': 5, 'cols': 40}),
            'date': DateInput(attrs={'type': 'date'}),
        }
    field_order = ['describtion', 'name', 'eventType', 'new_event_type', 'date', 'place', 'link', 'entry', 'image',
                   'is_capacity_limited', 'capacity', ]

    def clean(self):
        cleaned_data = super().clean()
        is_capacity_limited = cleaned_data.get('is_capacity_limited')
        capacity = cleaned_data.get('capacity')
        new_event_type = cleaned_data.get('new_event_type')

        if is_capacity_limited and capacity is None:
            self.add_error('capacity', 'Zadejte kapacitu, pokud je omezena.')

        if new_event_type and len(new_event_type) < 3:
            self.add_error('new_event_type', 'Typ události musí mít alespoň 3 znaky.')

        return cleaned_data

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

class EmailForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Zadejte zprávu'}),
        label='',  # Pokud nechcete název, můžete nechat prázdné
        required=True  # Povinné pole
    )

    def __init__(self, *args, include_subject=False, **kwargs):
        super().__init__(*args, **kwargs)
        if include_subject:
            self.fields['subject'] = forms.CharField(
                max_length=128,  # Maximální délka pro předmět
                label='Předmět',  # Název pole
                required=True,  # Povinné pole
                widget=forms.TextInput(attrs={'placeholder': 'Zadejte předmět'})  # Styl pro textové pole
            )