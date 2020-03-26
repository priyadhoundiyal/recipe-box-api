from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """ test the users API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ test creating user wuth valid payload is successful """
        payload = {
            'email': 'test@test.com',
            'password': "testpass",
            'name': "test user"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """ test creating user that already exists fails """
        payload = {
            'email': 'test@test.com',
            'password': "testpass",
            'name': 'Test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ tests that password must be more than 5 characters """
        payload = {
            'email': 'test@test.com',
            'password': "pw",
            'name': 'Test'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ test that a token is created for the user """
        payload = {'email': "testuser@test.com", 'password': "testpass"}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ test that token is not created for invalid credentials """
        create_user(email="testuser@test.com", password="testpass")
        payload = {'email': "testuser@test.com", 'password': "incorrect"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ tes tthat token is not created if user doesn't exist"""
        payload = {'email': "testuser@test.com", 'password': "incorrect"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ test that email and password are required """
        res = self.client.post(TOKEN_URL, {'email': 'test', 'password': ""})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
