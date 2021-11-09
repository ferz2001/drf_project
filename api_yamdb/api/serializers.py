from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',
        'first_name', 'last_name', 'confirmation_code',
        'bio', 'role')
        model = User