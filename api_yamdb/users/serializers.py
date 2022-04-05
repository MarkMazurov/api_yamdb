from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


class UserRegistationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        read_only_fields = ['role', 'password']
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value.lower() == ('me' * (len(value) // 2)):
            raise serializers.ValidationError(
                f'Имя {value} не может быть использованно')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ['password', 'confirmation_code']
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value.lower() == ('me' * (len(value) // 2)):
            raise serializers.ValidationError(
                f'Имя {value} не может быть использованно')
        return value


class CustomTokenSerializer(serializers.Serializer):
    """Получение токена"""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    @classmethod
    def get_tokens_for_user(cls, user):
        return RefreshToken.for_user(user)

    @staticmethod
    def validate_username(value):
        try:
            if CustomUser.objects.get(username=value):
                return value
        except CustomUser.DoesNotExist:
            massage = {'error': 'Не удается пройти аутентификацию с указанными'
                                ' учетными данными'}
            raise NotFound(massage)

    def validate(self, attrs):
        user = get_object_or_404(CustomUser, username=attrs['username'])
        if bool(attrs['confirmation_code'] == user.confirmation_code):
            refresh = self.get_tokens_for_user(user)
            return {'token': str(refresh.access_token)}
        raise serializers.ValidationError('Данные не прошли проверку')
