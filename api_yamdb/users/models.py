from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.SlugField(
        'Роль',
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True
    )

    class Meta:
        ordering = ['id']

    REQUIRED_FIELDS = ['email']

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        if self.is_superuser or self.is_staff:
            return True
        return self.role == self.ADMIN
