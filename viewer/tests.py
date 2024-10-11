from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event, EventType

User = get_user_model()

class EventTests(TestCase):

    def setUp(self):
        # Vytvoření uživatele a typu události pro testy
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.event_type = EventType.objects.create(name='Konference')
        self.event = Event.objects.create(
            title='Test Event',
            capacity=5,  # Kapacita pro testování
            eventType=self.event_type
        )

    def test_user_can_sign_up_for_event(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('event_sign_up', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.event.attendees.filter(id=self.user.id).exists())

    def test_user_can_cancel_registration(self):
        self.event.attendees.add(self.user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('event_cancel', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.event.attendees.filter(id=self.user.id).exists())

    def test_permissions_for_event(self):
        response = self.client.get(reverse('event_edit', args=[self.event.id]))
        self.assertEqual(response.status_code, 403)  # Očekáváme zákaz přístupu

    def test_event_data_validation(self):
        response = self.client.post(reverse('event_create'), {
            'name': '',  # Chybí název
            'image': ''  # Chybí obrázek
        })
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'image', 'This field is required.')

    def test_event_capacity_exceeded(self):
        # Přidáme maximální počet účastníků
        for i in range(self.event.capacity):
            self.event.attendees.add(User.objects.create_user(username=f'user{i}', password='testpass'))

        # Zkusíme přidat dalšího uživatele, což by mělo selhat
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('event_sign_up', args=[self.event.id]))
        self.assertEqual(response.status_code, 400)  # Očekáváme selhání kvůli překročení kapacity
        self.assertNotIn(self.user, self.event.attendees.all())