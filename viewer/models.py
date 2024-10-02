import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import (
    DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
    Model, TextField, BooleanField, ManyToManyField
)

class EventType(Model):
    name = CharField(max_length=128)

class Event(Model):
  name = CharField(max_length=128)
  describtion = CharField(max_length=128, default="")
  # time = DateTimeField
  #eventType = ManyToManyField(EventType)
  date = DateField(default=timezone.now)
  #create_date = DateTimeField(default=datetime.datetime.now)
  place = CharField(max_length=128, default="")
  entry = BooleanField(default=False)


class Comment(Model):
  comment = TextField(default="")
  event = ForeignKey(Event, on_delete=DO_NOTHING, default="")
  comment_date = DateTimeField(default=datetime.datetime.now)
  user = ForeignKey(User, on_delete=DO_NOTHING, default=1)



