from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event, EventType,Comment

class AttendeeInline(admin.TabularInline):
    model = Event.attendees.through  # Použij model ManyToMany relace
    extra = 1  # Kolik prázdných řádků pro přidání nových účastníků

class EventAdmin(admin.ModelAdmin):
    inlines = [AttendeeInline]
    exclude = ('create_date', 'attendees')  # Skryje tato pole v admin rozhraní

admin.site.register(EventType)
admin.site.register(Comment)
admin.site.register(Event, EventAdmin)