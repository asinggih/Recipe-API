from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe objects"""

    # list the ingredients and tags objects using its id only
    # not the whole freakin fields.
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,  # because its a many to many field
        queryset=Ingredient.objects.all(),  # this behaves like "select * from"
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "ingredients",
            "tags",
            "time_minutes",
            "price",
            "link",
        )
        read_only_fields = ('id',)
