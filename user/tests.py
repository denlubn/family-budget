from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient


CREATE_USER_URL = reverse("user-list")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            "username": "testuser",
            "email": "test1@test.com",
            "password": "testpass",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "tst",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_user_with_exist_username(self):
        """Test creating a user that already exists fails"""
        payload = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
