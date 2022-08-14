from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import RoleChoices


class User(AbstractUser):
    "Модель пользователя"
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=40, unique=True)

    password = models.CharField(max_length=20, blank=True, null=True)

    bio = models.TextField(
        "Биография",
        blank=True,
    )

    role = models.CharField(
        "Права",
        max_length=20,
        choices=[(tag.name, tag.value) for tag in RoleChoices],
        default=RoleChoices.USER.value,
    )

    confirmation_code = models.CharField(
        max_length=6,
        blank=True,
    )

    def __str__(self):
        return self.username
