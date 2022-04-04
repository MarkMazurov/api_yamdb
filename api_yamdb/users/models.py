from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import jwt
from users.validators import validate_birth_year

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        validators=[MinLengthValidator(5, message='Минимум 5 символов')])
    email = models.EmailField('Email адрес', unique=True)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    date_joined = models.DateTimeField('Дата создания', default=timezone.now)
    birth_year = models.IntegerField(blank=True, null=True,
                                     validators=[validate_birth_year])
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
        self.confirmation_code = make_password(confirmation_code)

    def set_password(self, password):
        self.password = password

    def __str__(self):
        return f'{self.username}, {self.email}'
