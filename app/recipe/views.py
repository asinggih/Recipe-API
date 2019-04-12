from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the db"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    # when we're defining a listmodelmixin we need to specify what to return
    # as a query set
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # this is for applying custom fields,
    # like limiting it to only authenticated users (which is
    # the user inside the request in thes case),
    # when the TagViewset is invoked from the URL
    def get_queryset(self):
        """return objects for the authenticated user only"""

        return self.queryset.filter(user=self.request.user).order_by('-name')
