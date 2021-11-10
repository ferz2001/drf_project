from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from .models import User

from backend.models import (Categorie,
                            Genre,
                            Title,
                            Review,
                            Comment)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = User


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Comment