from django.core.exceptions import ValidationError
from django.utils import timezone

VALIDATE_ERROR = {
    'error': 'Год больше нынешнего.'
}


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            VALIDATE_ERROR,
        )
