from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import generate_token


class ConfCodeSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=40)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        user = get_object_or_404(
            User, confirmation_code=data["confirmation_code"], username=data["username"]
        )
        return generate_token(user)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "role", "email")
        model = User
