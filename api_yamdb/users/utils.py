import random

from enum import Enum

from django.core import mail

from api_yamdb.settings import NOREPLY_EMAIL


class RoleChoices(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


def generate_conf_code():
    return str(random.randint(100000,999999))


def confirmation_mail(user_email_adress, conf_code):
    subject = 'confirmation code'
    for_whom = user_email_adress
    content = conf_code

    mail.send_mail(
        subject,
        content,
        NOREPLY_EMAIL,
        [for_whom,],
        fail_silently=False
    )

