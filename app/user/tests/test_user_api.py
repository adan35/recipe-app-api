"""
Test the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKER_URL = reverse('user:token')


def create_user(**params):
    """Creates and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test public feature of user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists(self):
        """Test an error is returned if the user already exists with the email"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_short_pass(self):
        """Test an error is returned if password is less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'tp',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user)

    def test_create_token_for_user(self):
        """Test generates token for valid user"""
        user_details = {
            'email': 'test@example.com',
            'password': 'goodpassword1',
            'name': 'Test Name',
        }
        create_user(**user_details)
        payload = {
            'email': 'test@example.com',
            'password': 'goodpassword1',
        }
        res = self.client.post(TOKER_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns an error if credentials are invalid"""
        user_details = {
            'email': 'test@example.com',
            'password': 'goodpassword1',
        }
        create_user(**user_details)
        payload = {
            'email': 'test@example.com',
            'password': 'badpass',
        }
        res = self.client.post(TOKER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test returns an error if password is blank"""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKER_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
