from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя основанная на AbstractUser."""
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        validators=[MinLengthValidator(5, message='Минимум 5 символов')])
    email = models.EmailField('Email адрес', unique=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    date_joined = models.DateTimeField('Дата создания', default=timezone.now)
    bio = models.CharField('Биография', max_length=200, blank=True)
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=10,
        default='user',
        error_messages={'role': 'Выбрана несуществующая роль'}
    )
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True, max_length=128
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def set_confirmation_code(self, confirmation_code):
        """Установка confirmation_code"""
        self.confirmation_code = confirmation_code

    def set_password_code(self, password):
        """Установка password"""
        self.password = password

    @property
    def is_user(self):
        """Проверить является ли пользователь 'user'."""
        return self.role == 'user'

    @property
    def is_moderator(self):
        """Проверить является ли пользователь 'moderator'."""
        return self.role == 'moderator'

    @property
    def is_admin(self):
        """Проверить является ли пользователь 'admin'."""
        return self.role == 'admin'

    def __str__(self):
        return f'{self.username}, {self.email}'
