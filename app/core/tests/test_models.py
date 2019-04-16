from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@email.com", password="password123"):
    """Create a sample user"""

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """Test creating new user with an email is successful"""

        email = "test@email.com"
        password = "password123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # this is the way to test the password in django
        self.assertTrue(user.check_password(password))

    def test_new_email_normalised(self):
        """Testing email for new user is normalised"""

        email = "test@RANDOMEMAIL.org"
        user = get_user_model().objects.create_user(
            email,
            password="password"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email"""

        # It should raise a ValueError
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                password="password"
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            'test@testemail.com',
            'password123'
        )

        # is_superuser is part of PermissionsMixin
        self.assertTrue(user.is_superuser)  # checks if user is superuser
        self.assertTrue(user.is_staff)      # checks if user is staff

    # because in django, we can specify which field
    # we wanna use when we call the str(modelObject)

    def test_tag_str(self):
        """test the tag string representation"""

        # create a new tag object
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="TestTag"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test the ingredient string representation"""

        ingredients = models.Ingredient.objects.create(
            user=sample_user(),
            name="Parsley"
        )

        self.assertEqual(str(ingredients), ingredients.name)
