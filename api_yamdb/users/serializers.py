from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from .models import User
from .utils import generate_token


class RegSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40)
    email = serializers.CharField(max_length=60)
    confirmation_code = serializers.CharField(max_length=6)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError
        if username == None:
            raise serializer.ValidationError
        
        return username

    class Meta:
        model = User
        fields = ('username', 'email', 'confirmation_code')


class ConfCodeSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=40)
    confirmation_code = serializers.CharField(max_length=6)

    def validate_confirmation_code(self, confirmation_code):
        
      #  user = get_object_or_404(
      #      User, confirmation_code=data["confirmation_code"], username=data["username"]
      #  )

        if not User.objects.filter(
                username=data.get('username'),
                confirmation_code=confirmation_code,
            ).exists():
            message = "wrong code"
            raise serializers.ValidationError

    
        return generate_token(user)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "role", "email")
        model = User
