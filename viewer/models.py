import datetime

from django.db.models import (
  DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
  Model, TextField, BooleanField, ManyToManyField
)

class EventType(Model):
  name = CharField(max_length=128)

class Event(Model):
  name = CharField(max_length=128)
  # date = DateField
  # place = CharField
  # time = DateTimeField
  # eventType = ManyToManyField(EventType, on_delete=DO_NOTHING)
  # entry = BooleanField

class Comment(Model):
  uzivatel = CharField(max_length=128, default="")
  comment = TextField(default="")
  event = ForeignKey(Event, on_delete=DO_NOTHING, default="")
  comment_date = DateTimeField(default=datetime.datetime.now)


