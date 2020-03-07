from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ test creating a user with email is successful """

        email = "test@test.com"
        password = "123456"
        user = get_user_model().objects.create_user(
            email=email,
            password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ tests that email for new user is normalized"""

        email = "testuser@DOMAIN.COM"
        user = get_user_model().objects.create_user(email, '123456')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ test creating new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 123456)

    def test_create_new_superuser(self):
        """ test creating new superuser """

        user = get_user_model().objects.create_superuser(
            "testsuper@domain.com",
            "123456",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
