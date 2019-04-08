from django.test import TestCase
# because we need user model for our test
from django.contrib.auth import get_user_model
from django.urls import reverse  # spits the url of a page given the view path


from rest_framework.test import APIClient
# human readable status codes
from rest_framework import status


# obtain the URL of user/create endpoint
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


# helper function to create user for our testing
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# seperate public user and logged in user test cases
class PublicUserApiTests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            'email': "test@testuser.com",
            'password': "password123",
            'name': "test name"
        }

        # check is status code returns 201 created
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # check if password is in the response data (it should not!!)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test creating a user that already exists"""

        payload = {
            'email': "test@testuser.com",
            'password': "password123",
            'name': "test name"
        }

        # override creating user by using our backend function
        # instead of via API endpoint
        create_user(**payload)

        # should return a bad request because
        # we already created the user
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 chars"""

        payload = {
            'email': "test@testuser.com",
            'password': "pw",
            'name': "test name"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # The user should also not be "already created"
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    # -------------------------------------------
    #           Token Unit Testing
    # -------------------------------------------

    def test_create_token_for_user(self):
        """Test if a token is created for the user"""

        payload = {
            'email': "test@testuser.com",
            'password': "password123",
            'name': "test name"
        }

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        """Test that token is not created with invalid creds"""

        create_user(
            email="test@testuser.com",
            password="testpassword"
        )

        payload = {
            'email': "test@testuser.com",
            'password': "wrongpassword",
            'name': "test name"
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token isn't created if user doesn't exist"""

        payload = {
            'email': "test@testuser.com",
            'password': "wrongpassword",
            'name': "test name"
        }

        # notice that we don't call the create_user function here

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required for token generation"""

        payload = {
            'email': "test@testuser.com",
            'password': ""
        }

        # notice that we don't call the create_user function here

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
