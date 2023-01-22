from django.db import models
from django.contrib.auth.models import AbstractUser
from .roles import UserRoles


class User(AbstractUser):
    """Класс пользователя."""

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=100,
        blank=False,
        unique=True
    )

    bio = models.TextField(
        verbose_name='О себе',
        max_length=512,
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        choices=UserRoles.choices(),
        default=UserRoles.user.name,
        blank=False,
    )

    class Meta:
        ordering = ['date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.email)

    @property
    def is_admin(self):
        return self.role == UserRoles.admin.name

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.name
