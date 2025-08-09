from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

    def test_user_registration(self):
        data = {
            "full_name": "Rhitika Pal",
            "email": "rhitika@example.com",
            "contact_number": "9801234567",
            "company_name": "Sasspire",
            "address": "Kathmandu",
            "industry": "Tech",
            "username": "rhitika",
            "password": "Rhitika@123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="rhitika").exists())

    def test_user_login_and_token_refresh(self):
        user = User.objects.create_user(
            username="rhitika",
            password="Rhitika@123",
            full_name="Rhitika Pal",
            email="rhitika@example.com",
            contact_number="9801234567",
            company_name="Sasspire",
            address="Kathmandu",
            industry="Tech"
        )
        login_data = {"username": "rhitika", "password": "Rhitika@123"}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        refresh_data = {"refresh": response.data["refresh"]}
        refresh_response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
