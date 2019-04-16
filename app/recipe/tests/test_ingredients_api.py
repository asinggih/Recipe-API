from django.test import TestCase
# because we need user model for our test
from django.contrib.auth import get_user_model
from django.urls import reverse  # spits the url of a page given the view path

from rest_framework.test import APIClient
# human readable status codes
from rest_framework import status

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredietns API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required to see ingredients"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedIngredientsApiTests(TestCase):
    """Test the priavte ingredients api can be retrieved by authorised user"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@testuser.com",
            password="testpassword"
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving a list of ingredietns"""

        Ingredient.objects.create(
            user=self.user,
            name="Parsley"
        )

        Ingredient.objects.create(
            user=self.user,
            name="Pepper"
        )

        res = self.client.get(INGREDIENTS_URL)

        # list all ingredients, sort by name in reverse order
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # making sure that what we retrieve is same as what we insert to db
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""

        user2 = get_user_model().objects.create_user(
            email="user2@testuser.com",
            password="testpassword"
        )

        Ingredient.objects.create(
            user=user2,
            name="eggplant"
        )

        ingredient = Ingredient.objects.create(
            user=self.user,
            name="Tumeric"
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
