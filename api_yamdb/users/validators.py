from rest_framework.exceptions import ValidationError
import datetime as dt


def validate_birth_year(self, value):
    year = dt.date.today().year
    if not (year - 123 < value <= year):
        raise ValidationError('Проверьте год рождения!')
    return value
