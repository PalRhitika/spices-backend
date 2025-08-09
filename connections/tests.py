from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from connections.models import Connection

class ConnectionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="alice", password="Alice@123",
            full_name="Alice", email="alice@example.com",
            contact_number="9801111111", company_name="Comp1",
            address="Address1", industry="Tech"
        )
        self.user2 = User.objects.create_user(
            username="bob", password="Bob@123",
            full_name="Bob", email="bob@example.com",
            contact_number="9802222222", company_name="Comp2",
            address="Address2", industry="Tech"
        )
        login_data = {"username": "alice", "password": "Alice@123"}
        token = self.client.post(reverse('token_obtain_pair'), login_data).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_search_users(self):
        url = reverse('user-search')
        response = self.client.get(url, {"q": "Bob"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_send_connection_request(self):
        url = reverse('send-request', args=[self.user2.user_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Connection.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    def test_accept_connection_request(self):
        connection = Connection.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.force_authenticate(user=self.user2)
        url = reverse('respond-request', args=[connection.id])
        response = self.client.post(url, {"action": "ACCEPTED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        connection.refresh_from_db()
        self.assertEqual(connection.status, "ACCEPTED")
