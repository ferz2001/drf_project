from rest_framework import permissions, serializers  # , validators
# from rest_framework.relations import SlugRelatedField

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

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'categorie')
        model = Title


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

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'categorie')
        model = Title


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
