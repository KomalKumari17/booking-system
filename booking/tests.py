from django.test import TestCase
from django.contrib.auth.models import User
from .models import Availability
from rest_framework.test import APIClient

class AvailabilityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_availability(self):
        avail = Availability.objects.create(
            user=self.user,
            day_of_week=0,
            start_time='09:00',
            end_time='12:00'
        )
        self.assertEqual(str(avail), "testuser - Monday 09:00-12:00")

class AvailabilityAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_availability_api(self):
        response = self.client.post('/api/availability/', {
            "day_of_week": 0,
            "start_time": "09:00",
            "end_time": "12:00"
        }, format='json')
        self.assertEqual(response.status_code, 201)