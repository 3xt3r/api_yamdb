from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

VALIDATE_ERROR = {
    'error': 'Невозможно выбрать данный никнейм.'
}


def username_not_me(value):
    me = 'me'
    if value == me:
        raise serializers.ValidationError(VALIDATE_ERROR)


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('%(value)s год больше текущего'),
            params={'value': value},
        )
