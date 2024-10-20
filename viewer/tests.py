from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event, EventType
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

User = get_user_model()

class EventTests(TestCase):

    def setUp(self):
        # Vytvoření uživatele a typu události pro testy
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.event_type = EventType.objects.create(name='Konference')
        self.event = Event.objects.create(
            name='Test Event',
            describtion="popis události",
            is_capacity_limited= True,
            capacity=5  # Kapacita pro testování
        )
        self.event.eventType.set([self.event_type])  # Nastavení typu události

    def test_user_can_sign_up_for_event(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('attendees', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.event.attendees.filter(id=self.user.id).exists())
        content_str = response.content.decode('utf-8')
        self.assertIn("přihlásili", content_str)

    def test_user_can_cancel_registration(self):
        self.event.attendees.add(self.user)
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('attendees', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.event.attendees.filter(id=self.user.id).exists())
        content_str = response.content.decode('utf-8')
        self.assertIn("odhlásili", content_str)

    def test_permissions_for_event(self):
        response = self.client.get(reverse('event_update', args=[self.event.id]))
        self.assertEqual(response.status_code, 400)  # Očekáváme zákaz přístupu
        self.assertNotIn(self.user, self.event.attendees.all())

    def test_event_data_validation(self):
        # Odeslání POST požadavku s prázdnými povinnými poli
        response = self.client.post(reverse('event_create'), {
            'name': '',  # Chybí název
            'image': ''  # Chybí obrázek
        })

        # Ověření, že formulář obsahuje chyby
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'image', 'This field is required.')

        # Ověření, že událost nebyla vytvořena
        self.assertEqual(Event.objects.count(), 0)

    def test_event_capacity_exceeded(self):
        # Přidáme maximální počet účastníků
        for i in range(self.event.capacity):
            self.event.attendees.add(User.objects.create_user(username=f'user{i}', password='testpass'))

        # Zkusíme přidat dalšího uživatele, což by mělo selhat
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('attendees', args=[self.event.id]), follow=True)
        self.assertRedirects(response, '/detail/1')
        # Očekáváme selhání kvůli překročení kapacity, vypsání hlášky a přesměrování
        content_str = response.content.decode('utf-8')
        self.assertIn("Nelze", content_str)


# pip install selenium

class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the WebDriver (make sure the path is correct if needed)
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    def test_login(self):
        # Access the live server URL
        self.selenium.get(f'{self.live_server_url}/login/')
        time.sleep(2)
        # Find the username and password input fields and fill them
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        time.sleep(2)
        # Submit the form
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)
        # Test that we successfully logged in (check for a successful redirect or message)
        self.assertIn("MŮJ ÚČET - admin", self.selenium.page_source)

