import random
from enum import Enum

from api_yamdb.settings import NOREPLY_EMAIL
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken


class RoleChoices(Enum):
    #   name    value
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


def email_check(email):
    """Валидация почты."""
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def generate_conf_code():
    """Генерирует случайный код подтверждения."""
    return str(random.randint(100000, 999999))


def confirmation_mail(user_email_adress, conf_code):
    """Составляет и отправляет email с кодом."""
    subject = "confirmation code"
    for_whom = user_email_adress
    content = conf_code

    mail.send_mail(
        subject,
        content,
        NOREPLY_EMAIL,
        [
            for_whom,
        ],
        fail_silently=False,
    )


def generate_token(user):
    """Генерирует новый токен для пользователя."""
    new_token = RefreshToken.for_user(user)

    return {
        "access": str(new_token.access_token),
    }
