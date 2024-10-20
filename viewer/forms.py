from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from viewer.models import Event, EventType, User, Comment
from django.test import TestCase
import re
from django.forms.widgets import Textarea, DateInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.core.exceptions import ValidationError

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

    def validate_place(value):
        if not value.isalpha():
            raise ValidationError('Pole "Místo" může obsahovat pouze písmena.')
        if not value[0].isupper():
            raise ValidationError('První znak v poli "Místo" musí být velké písmeno.')

    place = forms.CharField(
        max_length=100,
        validators=[validate_place],
        label='Místo'
    )
    class Meta:
        model = Event
        fields = ['name', 'describtion', 'eventType', 'date', 'place', 'link', 'entry', 'image', 'is_capacity_limited', 'capacity', 'new_event_type']
        labels = dict(name='Název', describtion='Popis', eventType='Typ akce', date='Datum', place='Místo',
                      link='Odkaz', entry='Vstupné', image='Obrázek')

        widgets = {
            'describtion': Textarea(attrs={'rows': 5, 'cols': 40}),
            'date': DateInput(attrs={'type': 'date'}),
        }
    field_order = ['describtion', 'name', 'eventType', 'new_event_type', 'date', 'link', 'entry', 'image',
                   'is_capacity_limited', 'capacity', 'place'  ]


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


class EventTests(TestCase):

    def setUp(self):
        # Vytvoření uživatele a typu události pro testy
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.event_type = EventType.objects.create(name='Konference')
        self.event = Event.objects.create(
            name='Test Event',
            describtion="popis události",
            is_capacity_limited= True,
            capacity=5  # Kapacita pro testování
        )
        self.event.eventType.set([self.event_type])  # Nastavení typu události

    def test_user_can_sign_up_for_event(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('attendees', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.event.attendees.filter(id=self.user.id).exists())

    def test_user_can_cancel_registration(self):
        self.event.attendees.add(self.user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('attendees', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.event.attendees.filter(id=self.user.id).exists())

    def test_permissions_for_event(self):
        response = self.client.get(reverse('event_update', args=[self.event.id]))
        self.assertEqual(response.status_code, 400)  # Očekáváme zákaz přístupu
        self.assertNotIn(self.user, self.event.attendees.all())

    def test_event_data_validation(self):
        response = self.client.post(reverse('event_create'), {
            'name': '',  # Chybí název
            'image': ''  # Chybí obrázek
        })
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'image', 'This field is required.')

    def test_event_capacity_exceeded(self):
        # Přidáme maximální počet účastníků
        for i in range(self.event.capacity):
            self.event.attendees.add(User.objects.create_user(username=f'user{i}', password='testpass'))

        # Zkusíme přidat dalšího uživatele, což by mělo selhat
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('attendees', args=[self.event.id]), follow=True)
        self.assertRedirects(response, '/detail/1')
        # Očekáváme selhání kvůli překročení kapacity, vypsání hlášky a přesměrování
        content_str = response.content.decode('utf-8')
        self.assertIn("Nelze", content_str )
        #self.assertEqual(self.event.attendees.filter(id=self.user.id).exists(), False)