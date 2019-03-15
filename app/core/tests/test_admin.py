from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse  # spits the url of a page given the view path


class AdminSiteTests(TestCase):

    # Create a setUp function to pave for other functions.
    # It will be run before every test that we run
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="password123"
        )
        # Use the CLient helper function to log a user in
        # with the Django authentication automatically.
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="regular@test.com",
            password="password123",
            name="Regular Test User"
        )

    # we need to test it because we need to slightly customise
    # django admin to work with our user model
    def test_users_listed(self):
        """Test if users are listed on user page"""

        # will generate url for our "list user" page
        # the url is documented in django admin docs
        #   app_that_we_use:url_that_we_want
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # It also checks that it's a HTTP 200 OK,
        # which includes our required response and the content.
        # Can't fake the response up there with a string
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""

        # admin/core/user/1 or 2 or whatever it is
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Just check if the requrest to that user edit page is ok
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        # Just check if the requrest to that user edit page is ok
        self.assertEqual(res.status_code, 200)
