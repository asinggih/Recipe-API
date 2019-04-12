from django.test import TestCase
# because we need user model for our test
from django.contrib.auth import get_user_model
from django.urls import reverse  # spits the url of a page given the view path

from rest_framework.test import APIClient
# human readable status codes
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer


# we're gonna be using Viewset, that automatically
# appends the action name to the end of the url for us, using the router
TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving tags"""

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedApiTests(TestCase):
    """Test the authorised user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@testuser.com",
            password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_tags(self):
        """Test retrieving tags"""

        # creating tag objects for testing
        Tag.objects.create(
            user=self.user,
            name="Vegan"
        )

        Tag.objects.create(
            user=self.user,
            name="MainCourse"
        )

        res = self.client.get(TAGS_URL)

        # alphabetical reverse order, based on the name
        tags = Tag.objects.all().order_by('-name')
        # serializign our objects, consisting of several tags
        # so that we can compare it with the data from the response
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """Test that tags returned are for authenticated users only"""

        # create a new user2 for testing
        user_two = get_user_model().objects.create_user(
            email="u2@testuser.com",
            password="testpassword"
        )

        Tag.objects.create(
            user=user_two,
            name="HotFood"
        )

        tag = Tag.objects.create(
            user=self.user,
            name="Comfrot Food"
        )

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # make sure that it only returns 1 data
        self.assertEqual(len(res.data), 1)
        # the response returned by the server is our tag f
        # rom the authenticated user
        self.assertEqual(res.data[0]['name'], tag.name)
