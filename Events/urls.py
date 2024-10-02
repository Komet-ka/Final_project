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

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views

from viewer.views import detail, my_page, main_page

from viewer.views import (EventsView, EventCreateView, EventUpdateView, EventDeleteView,
                          EventTypeView, EventTypeCreateView, EventTypeUpdateView,
                          EventTypeDeleteView, SubmittablePasswordChangeView, SignUpView,
                          UserUpdateView, EventFilterView)

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Comment)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', main_page, name='main_page'),
    path('', main_page, name='main_page'),  # Class based view
    path('detail/<pk>', detail),
    path('type_filter/', EventFilterView.as_view(), name='type_filter'),

    path('events/', EventsView.as_view(), name='events'),
    path('events/create', EventCreateView.as_view(), name='event_create'),
    path('events/update/<pk>', EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<pk>', EventDeleteView.as_view(), name='event_delete'),

    path('types/', EventTypeView.as_view(), name='types'),
    path('type/create', EventTypeCreateView.as_view(), name='type_create'),
    path('type/update/<pk>', EventTypeUpdateView.as_view(), name='type_update'),
    path('type/delete/<pk>', EventTypeDeleteView.as_view(), name='type_delete'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('my_page/', my_page, name='my_page'),
    path('my_page/update/', UserUpdateView.as_view(), name='user_update'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
]
