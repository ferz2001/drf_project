from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from backend.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = User