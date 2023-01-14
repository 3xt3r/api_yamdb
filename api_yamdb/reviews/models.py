import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator,
    RegexValidator,
)
from .validators import year_validator


class User(AbstractUser):
    """Класс пользователя."""

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
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
    )
    confirmation_code = models.TextField(
        verbose_name='Код подтверждения',
        max_length=100,
        default=str(uuid.uuid4()),
        null=True,
        editable=False,
    )

    class Meta:
        ordering = ['date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.email)

    @property
    def is_admin(self):
        return self.role == (settings.ADMIN_ROLE or self.is_staff
        or self.is_superuser
    )

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR_ROLE


class Category(models.Model):
    """Класс категории."""

    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Класс жанра."""

    name = models.CharField(
        verbose_name='Жанр',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True,

        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Класс названия."""

    name = models.TextField(
        verbose_name='Название произведения',
        max_length=256, db_index=True,
    )

    year = models.PositiveIntegerField(
        verbose_name='Год произведения',
        validators=[year_validator],
    )
    description = models.TextField(verbose_name='Описание',
                                   null=True, blank=True,)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Класс отзывов."""

    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор'
    )
    score = models.IntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Класс комментария."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст комментария',)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария',
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
