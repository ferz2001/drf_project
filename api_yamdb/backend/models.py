from api.utilities import get_confirmation_code
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [('USER', 'user'),
                ('MODERATOR', 'moderator'),
                ('ADMIN', 'admin')]


class User(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False, null=False)
    email = models.EmailField(max_length=254,
                              unique=True, blank=False, null=False)
    password = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(max_length=20, default=get_confirmation_code())
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER',
    )


class Categorie(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(max_length=50, unique=True,)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(max_length=50, unique=True,)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=70,)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True,)
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    categorie = models.ForeignKey(
        'Categorie',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    
    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.PositiveIntegerField(
        'Оценка',)
    text = models.CharField(max_length=256,)
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
