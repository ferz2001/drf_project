from rest_framework import serializers
import datetime as dt
from django.db.models import Avg

from reviews.models import (Categorie,
                            Genre,
                            Title,
                            Review,
                            Comment,
                            User)



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = ('__all__')
        fields = (
            'bio', 'email', 'first_name', 'last_name', 'role', 'username')
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
    category = CategorieSerializer(source='categorie')
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return None
        else:
            return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(),
        slug_field='slug',
        source='categorie'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category'
        )
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
        exclude = ('title',)
        model = Review
        read_only_fields = ('title', 'category', 'genre')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        exclude = ('title', 'review')
        model = Comment
        read_only_fields = ('title', 'review')
