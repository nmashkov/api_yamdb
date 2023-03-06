from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 1
    MODERATOR = 2
    USER = 3

    ROLES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.PositiveSmallIntegerField(
        'Роль',
        choices=ROLES,
        blank=True,
        default=3
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True
    )

    REQUIRED_FIELDS = ['email']
