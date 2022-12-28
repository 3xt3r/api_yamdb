import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = settings.USER_ROLE
    MODERATOR = settings.MODERATOR_ROLE
    ADMIN = settings.ADMIN_ROLE
    ROLE_CHOISES = [
        (USER, settings.USER_ROLE),
        (MODERATOR, settings.MODERATOR_ROLE),
        (ADMIN, settings.ADMIN_ROLE)
    ]
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    email = models.EmailField(
        verbose_name='Электронная почта',
        blank=False,
        unique=True
    )

    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
    )
    confirmation_code = models.TextField(
        verbose_name='Код подтверждения',
        max_length=100,
        default=uuid.uuid4,
        null=True,
        editable=False,
    )

    class Meta:
        ordering = ['date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.email)

    #Проверка на права администратора
    @property
    def is_admin(self):
        return self.role == settings.ADMIN_ROLE or self.is_staff

    #Проверка на права модератора
    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR_ROLE
