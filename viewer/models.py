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
    is_approved = models.BooleanField(default=False)  # Výchozí hodnota je False (neschváleno)

    class Meta:
        permissions = [
            ('custom_add_eventtype', 'Can add event type'),  # změňte název na něco jedinečného
        ]
    def __str__(self):
        return self.name

class Event(Model):
  name = CharField(max_length=128)
  describtion = CharField(max_length=6000, default="")
  eventType = ManyToManyField(EventType)
  date = DateField(default=timezone.now)
  create_date = DateTimeField(auto_now_add=True)
  place = CharField(max_length=128, default="")
  entry = BooleanField(default=False)
  user = ForeignKey(User, on_delete=DO_NOTHING, default=1)
  link = URLField(max_length=200, blank=True, null=True)
  image = ImageField(upload_to='event_images/', blank=False, null=True)
  attendees = models.ManyToManyField(User, related_name="events_attending", blank=True)
  # Nové pole pro maximální kapacitu
  capacity = models.PositiveIntegerField(null=True, blank=True, default=None)  # None znamená neomezeno
  # Pole pro indikaci, zda je kapacita omezena
  is_capacity_limited = models.BooleanField(default=False)
  # Nové pole pro schválení administrátorem
  is_approved = models.BooleanField(default=False)  # Výchozí hodnota je False (ne schváleno)

  def __str__(self):
      return self.name


class Comment(Model):
  comment = CharField(max_length=500)
  event = ForeignKey(Event, on_delete=models.CASCADE, default="")
  comment_date = models.DateTimeField(default=timezone.now)
  user = ForeignKey(User, on_delete=models.CASCADE, default=1)



