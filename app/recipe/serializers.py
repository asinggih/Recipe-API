from rest_framework import serializers
from core.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    # Meta class to know which model that we need,
    # what fields that we need (we need to explicitly add this),
    # and extra options like write only fields, etc.
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id', )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient objects"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id', )
