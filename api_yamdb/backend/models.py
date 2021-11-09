from django.db import models
from api.models import User


class Categorie(models.Model):
    name = models.CharField(max_length=256, required=True)
    slug = models.SlugField(max_length=50, unique=True, required=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, required=True)
    slug = models.SlugField(max_length=50, unique=True, required=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=70, required=True)
    year = models.PositiveIntegerField(max_length=4, required=True)
    slug = models.SlugField(max_length=50, unique=True, required=True)
    description = models.TextField(blank=True, required=False)
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        required=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.PositiveIntegerField(
        'Оценка', required=True)
    text = models.CharField(max_length=256, required=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text
