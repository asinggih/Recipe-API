from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttr(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Base Viewset for user owned recipte attributes"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    # queryset and serializer_class will be filled by each of the
    # classes, since they have different values.

    # this is for applying custom fields,
    # like limiting it to only authenticated users (which is
    # the user inside the request in thes case),
    # when the TagViewset is invoked from the URL
    def get_queryset(self):
        """return objects for the authenticated user only"""

        filtered_queryset = self.queryset.filter(
            user=self.request.user
        )

        return filtered_queryset.order_by('-name')

    # overrides the perform_create so that we can assign
    # the tag to the correct user
    def perform_create(self, serializer):
        """Create a new object"""
        # setting the user to the authenticated user in the
        # http request
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    """Manage tags in the db"""

    # when we're defining a listmodelmixin we need to specify what to return
    # as a query set
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    """Manage Ingredients in db"""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewset(viewsets.ModelViewSet):
    """Manage Recipe in the db"""

    # the default action is list
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """return objects for authenticated user only"""

        filtered_queryset = self.queryset.filter(
            user=self.request.user
        )

        return filtered_queryset

    # change a serializer class for a particular request.
    # This is the function that we wanna use to handle
    # different actions available in our viewset
    # e.g., list, or retrieve, etc etc.
    def get_serializer_class(self):
        """return appropriate serializer class"""

        # check the action for the current requets
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """create and return a new object"""

        serializer.save(user=self.request.user)
