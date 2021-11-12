from rest_framework import permissions, serializers  # , validators
# from rest_framework.relations import SlugRelatedField
import datetime as dt
from django.db.models import Avg

from backend.models import (Categorie,
                            Genre,
                            Title,
                            Review,
                            Comment,
                            User)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = User


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categorie


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'categorie'
        )
        model = Title

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return 'None'
        else:
            return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleWriteSerializer(serializers.ModelSerializer):
    categorie = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'categorie')
        model = Title

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return 'None'
        else:
            return obj.reviews.aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        now_year = dt.date.today().year
        if value > now_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Review
        read_only_fields = ('title', 'category', 'genre')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Comment
        read_only_fields = ('title', 'review')
