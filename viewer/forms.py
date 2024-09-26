from django.forms import ModelForm
from viewer.models import Event, EventType
import re

class EventForm(ModelForm):

  class Meta:
    model = Event
    fields = '__all__'

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