import datetime

from django.forms import ImageField
from django.utils import timezone

from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import (
    DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
    Model, TextField, BooleanField, ManyToManyField, URLField, ImageField
)

class EventType(Model):
    name = CharField(max_length=128)

    class Meta:
        permissions = [
            ('custom_add_eventtype', 'Can add event type'),  # změňte název na něco jedinečného
        ]
    def __str__(self):
        return self.name

class Event(Model):
  name = CharField(max_length=128)
  describtion = CharField(max_length=128, default="")
  eventType = ManyToManyField(EventType)
  date = DateField(default=timezone.now)
  create_date = DateTimeField(auto_now_add=True)
  place = CharField(max_length=128, default="")
  entry = BooleanField(default=False)
  user = ForeignKey(User, on_delete=DO_NOTHING, default=1)
  link = URLField(max_length=200, default="")
  image = ImageField(upload_to='event_images/', blank=True, null=True)  # Přidáno pole pro obrázek
  attendees = models.ManyToManyField(User, related_name="events_attending", blank=True)

  def __str__(self):
      return self.name


class Comment(Model):
  comment = TextField(default="")
  event = ForeignKey(Event, on_delete=DO_NOTHING, default="")
  comment_date = DateTimeField(default=datetime.datetime.now)
  user = ForeignKey(User, on_delete=DO_NOTHING, default=1)



