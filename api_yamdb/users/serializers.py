from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
import datetime as dt

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ['role']
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Имя {value} не может быть использованно')
        return value

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if not (year - 123 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value
