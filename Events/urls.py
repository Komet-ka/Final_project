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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LoginView
from django.contrib.auth import views
from django.contrib.auth import views as auth_views

from viewer.views import (detail, my_page, main_page, logout_view, attendees, search_view, api_upcoming_events,
                          list_events, delete_comment, SendEmailToAllView, SendEmailToAttendeeView)
from viewer.views import (EventsView, EventCreateView, EventUpdateView, EventDeleteView,
                          EventTypeView, EventTypeCreateView, EventTypeUpdateView,
                          EventTypeDeleteView, SubmittablePasswordChangeView, SignUpView,
                          UserUpdateView, MyEventsView, EventFilterByTypeView)

handler403 = 'viewer.views.custom_403_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_page/', main_page, name='main_page'),
    path('', main_page, name='main_page'),  # Class based view
    path('detail/<pk>', detail, name='detail'),
    path('type_filter/<pk>', EventFilterByTypeView.as_view(), name='type_filter'),
    path('administrace/', EventTypeView.as_view(), name='administrace'),

    path('events/', EventsView.as_view(), name='events'),
    path('events/create', EventCreateView.as_view(), name='event_create'),
    path('events/update/<pk>', EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<pk>', EventDeleteView.as_view(), name='event_delete'),

    path('type/create', EventTypeCreateView.as_view(), name='type_create'),
    path('type/update/<pk>', EventTypeUpdateView.as_view(), name='type_update'),
    path('type/delete/<pk>', EventTypeDeleteView.as_view(), name='type_delete'),

    path('my_page/', my_page, name='my_page'),
    path('my_page/update/', UserUpdateView.as_view(), name='user_update'),
    path('attendees/<pk>', attendees, name='attendees'),
    path('my_attendees/', MyEventsView.as_view(), name='my_attendees'),

    path('send_email/<int:attendee_id>/<int:event_pk>/', SendEmailToAttendeeView.as_view(), name='send_email'),
    path('send_email_to_all/<int:event_pk>/', SendEmailToAllView.as_view(), name='send_email_to_all'),

    path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('search/', search_view, name='search'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

    path('api/get/all_events/', api_upcoming_events, name='api_upcoming_events'),
    path('list_events/', list_events, name='list_events'), #tohle je v jiné aplikaci
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

