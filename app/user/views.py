from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # serializer_class is a django variable name as
    # it has been defined in the docs
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    # so that we can login from our browser, and see the token
    # otherwise we hv to make the HTTP post request using burp or something
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # overriding the get_object function to return the particular
    # authenticated user
    def get_object(self):
        """Retrieve and return authenticated user"""
        # when get object is called, request will have the
        # user, because of the authentication_classes that
        # takes care of getting the authenticated user,
        # and assigning it to request
        return self.request.user
