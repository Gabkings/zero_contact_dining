import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Validates phone numbers in international or local format.
    """

    pattern = r"^(\+?[0-9]{10,15})$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Enter a valid phone number."
        )
    
