# notifications/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from notifications.models import Notification

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="Test@1234",
            full_name="Test User",
            email="test@example.com",
            contact_number="9801234567",
            company_name="TestCo",
            address="Kathmandu",
            industry="Tech"
        )
        login_data = {"username": "testuser", "password": "Test@1234"}
        token = self.client.post(reverse('token_obtain_pair'), login_data).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.notifications_url = reverse("notifications-list")

    def test_list_notifications(self):
        Notification.objects.create(user=self.user, message="Test notification")
        response = self.client.get(self.notifications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_create_notification(self):
        data = {"message": "New notification"}
        response = self.client.post(self.notifications_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)

    def test_mark_as_read(self):
        notif = Notification.objects.create(user=self.user, message="Mark me read")
        url = reverse("notifications-detail", args=[notif.id])  # fixed
        response = self.client.patch(url, {"is_read": True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_delete_notification(self):
        notif = Notification.objects.create(user=self.user, message="Delete me")
        url = reverse("notifications-detail", args=[notif.id])  # fixed
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)
