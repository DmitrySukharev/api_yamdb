from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import RoleChoices


class User(AbstractUser):
    "Модель пользователя"

    bio = models.TextField(
        "Биография",
        blank=True,
    )

    role = models.CharField(
        "Права",
        max_length=20,
        choices=[(tag, tag.value) for tag in RoleChoices],
        default="user",
    )

    confirmation_code = models.CharField(
        max_length=60,
        blank=True
    )

    def __str__(self):
        return self.username
