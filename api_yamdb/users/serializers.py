from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import generate_token


class ConfCodeSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=40)
    confirmation_code = serializers.CharField(max_length=6)

    def validate_confirmation_code(self, confirmation_code):
        if not User.objects.filter(
                confirmation_code=confirmation_code,
            ).exists():
            message = "wrong code"
            raise serializers.ValidationError
    
        return confirmation_code

    def validate_username(self, username):
        get_object_or_404(User, username=username)

            return serializers.ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "role", "email")
        model = User
