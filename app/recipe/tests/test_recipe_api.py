from django.test import TestCase
# because we need user model for our test
from django.contrib.auth import get_user_model
from django.urls import reverse  # spits the url of a page given the view path

from rest_framework.test import APIClient
# human readable status codes
from rest_framework import status

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


# /api/recipe/recipes
RECIPES_URL = reverse("recipe:recipe-list")

# /api/recipe/recipes/1/


def detail_url(recipe_id):
    """Return recipe detail URL"""

    # name of the endpoint that the default router
    # will create for our viewset
    return reverse("recipe:recipe-detail", args=[recipe_id])


def sample_tag(user, name="Main Course"):
    """create and return a sample tag"""

    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Parsley"):
    """create and return a sample ingredeint"""

    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create and return a sample recipe"""

    defaults = {
        "title": "Sample recipe",
        "time_minutes": 10,
        "price": 5.00
    }
    # take whatever key in params and update them
    # or create a new entry if it doesnt exist
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRecipeApiTest(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="test@testuser.com",
            password="testpassword"
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """test retrieveing list of recipes"""

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that recipes for the authenticated user are returned"""

        user2 = get_user_model().objects.create_user(
            email="user2@testuser.com",
            password="testpassword"
        )

        # one is authenticated user, one is unauthenticated user
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        # filter recipe by authenticated users
        recipes = Recipe.objects.filter(user=self.user)
        # even though we will only get one, we still pass many = true
        # so that we can get a list view
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""

        recipe = sample_recipe(user=self.user)
        # add tags to our recipe object
        recipe.tags.add(sample_tag(user=self.user))
        # add ingredients to our recipe object
        recipe.ingredients.add(sample_ingredient(user=self.user))

        # generate the URL
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating a basic recipe"""

        payload = {
            'title': 'Deepfried Tofu',
            'time_minutes': 15,
            'price': 3.00,
        }

        res = self.client.post(RECIPES_URL, payload)

        # standard HTTP statuscode on API when successfully
        # creating the request
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get recipe object with the id from our response.data
        recipe = Recipe.objects.get(id=res.data['id'])

        # check if each value in the payload is the same as
        # value in our retrieved object from the response
        for key in payload:
            # getattr(recipe, key) is equal to
            # dictionary[key], however, this is for objects
            # not dicts
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_creating_recipe_with_tags(self):
        """Test creating recipe with tags"""

        tag1 = sample_tag(user=self.user, name="Meat Lover")
        tag2 = sample_tag(user=self.user, name="Main Course")

        payload = {
            'title': "Deepfried bacon",
            'tags': [tag1.id, tag2.id, ],
            'time_minutes': 60,
            'price': 20.00,
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        # storing all tags of the recipe
        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_creating_recipe_with_ingredients(self):
        """Test creating recipe wiht ingredients"""

        ing1 = sample_ingredient(user=self.user, name="Parsley")
        ing2 = sample_ingredient(user=self.user, name="Mushroom")

        payload = {
            'title': "Stir fried mushrooms",
            'ingredients': [ing1.id, ing2.id],
            'time_minutes': 15,
            'price': 5.00,
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ing1, ingredients)
        self.assertIn(ing2, ingredients)
