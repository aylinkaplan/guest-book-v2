from django.test import TestCase

# your_app/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Entry
from .serializers import UserSerializer, EntrySerializer


class EntryTests(APITestCase):
    def setUp(self):
        self.create_entry_url = reverse('create-entry')
        self.user_list_url = reverse('list-user')
        self.entry_list_url = reverse('list-entry')

    def test_create_entry(self):
        data = {
            "user": {"name": "New User"},
            "subject": "New Entry",
            "message": "This is a new entry."
        }
        response = self.client.post(self.create_entry_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().name, "New User")
        self.assertEqual(Entry.objects.first().subject, "New Entry")

    def test_get_users(self):
        user = User.objects.create(name="New User")
        Entry.objects.create(user=user, subject="Subject 1", message="Message 1")
        Entry.objects.create(user=user, subject="Subject 2", message="Message 2")

        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 1)
        self.assertEqual(response.data['users'][0]['total_messages'], 2)
        self.assertEqual(response.data['users'][0]['last_entry'], "Subject 2 | Message 2")

    def test_get_entries(self):
        user = User.objects.create(name="New User")
        Entry.objects.create(user=user, subject="Entry 1", message="Message 1")
        Entry.objects.create(user=user, subject="Entry 2", message="Message 2")
        Entry.objects.create(user=user, subject="Entry 3", message="Message 3")
        Entry.objects.create(user=user, subject="Entry 4", message="Message 4")

        response = self.client.get(self.entry_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['entries']), 3)

