import datetime

from django.db.models import (
  DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
  Model, TextField, BooleanField, ManyToManyField
)

class EventType(Model):
  name = CharField(max_length=128)

class Event(Model):
  name = CharField(max_length=128)
  describtion = CharField(max_length=128, default="")
  # date = DateField
  # place = CharField
  # time = DateTimeField
  # eventType = ManyToManyField(EventType, on_delete=DO_NOTHING)
  # entry = BooleanField

from django.contrib.auth import get_user_model
User = get_user_model()
class Comment(Model):
  comment = TextField(default="")
  event = ForeignKey(Event, on_delete=DO_NOTHING, default="")
  comment_date = DateTimeField(default=datetime.datetime.now)
  user = ForeignKey(User, on_delete=DO_NOTHING, default=1)



