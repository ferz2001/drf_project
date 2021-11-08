from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


    

class User(AbstractUser):
    
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False, null=False)
    email = models.EmailField(max_length=254,
                              unique=True, blank=False, null=False)

    bio = models.TextField(blank=True)

    ROLE_CHOICES = [('USER', 'user'),
    ('MODERATOR', 'moderator'), ('ADMIN', 'admin')]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER',
    )
