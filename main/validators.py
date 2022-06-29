
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils import timezone


def validate_digit_length(ISBN):
    if not (ISBN.isdigit() and len(ISBN) == 13):
        raise ValidationError('%(ISBN)s must be 13 digits', params={'ISBN': ISBN}, )


def month():
    return timezone.now() + timezone.timedelta(days=30)
