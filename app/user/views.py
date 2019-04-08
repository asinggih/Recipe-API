from rest_framework import generics
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
