from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from viewer.models import Event, EventType, User
import re
from django.forms.widgets import Textarea, DateInput

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


class SignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = ['username', 'first_name', 'last_name']

  def save(self, commit=True):
    self.instance.is_active = True
    return super().save(commit)


class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']

class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'describtion', 'eventType', 'date', 'place', 'entry']
    widgets = {
        'describtion': Textarea(attrs={'rows': 5, 'cols': 40}),
        'date': DateInput(attrs={'type': 'date'})  # Kalendář pro výběr data
    }