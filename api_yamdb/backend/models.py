from api.utilities import get_confirmation_code
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLE_CHOICES = [('user', 'user'),
                ('moderator', 'moderator'),
                ('admin', 'admin')]


class User(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False, null=False)
    email = models.EmailField(max_length=254,
                              unique=True, blank=False, null=False)
    password = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(
        max_length=20, default=get_confirmation_code())
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER',
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == ROLE_CHOICES[2][1]

    @property
    def is_moderator(self):
        return self.role == ROLE_CHOICES[1][1]


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
    genre = models.ManyToManyField(
        'Genre',
        # on_delete=models.SET_NULL,
        related_name='titles',
        # null=True,
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
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        blank=False,
        null=False
    )
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
