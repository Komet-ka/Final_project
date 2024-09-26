"""Events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from viewer.models import Event, EventType, Comment

from viewer.views import detail

from viewer.views import (EventsView, EventCreateView, EventUpdateView, EventDeleteView,
                          EventTypeView, EventTypeCreateView, EventTypeUpdateView, EventTypeDeleteView)

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Comment)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', EventsView.as_view()),
    path('', EventsView.as_view(), name='main_page'),  # Class based view
    path('detail/<pk>', detail),

    path('main_page/create', EventCreateView.as_view(), name='event_create'),
    path('main_page/update/<pk>', EventUpdateView.as_view(), name='event_update'),
    path('main_page/delete/<pk>', EventDeleteView.as_view(), name='event_delete'),

    path('types', EventTypeView.as_view(), name='types'),
    path('type/create', EventTypeCreateView.as_view(), name='type_create'),
    path('type/update/<pk>', EventTypeUpdateView.as_view(), name='type_update'),
    path('type/delete/<pk>', EventTypeDeleteView.as_view(), name='type_delete'),
]
