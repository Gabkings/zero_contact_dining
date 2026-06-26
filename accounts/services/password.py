from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction


class PasswordService:
    """
    Handles password operations.
    """

    @staticmethod
    @transaction.atomic
    def change_password(user, new_password):
        """
        Change a user's password.
        """

        validate_password(new_password, user)

        user.set_password(new_password)

        user.save(update_fields=["password"])

        return user

    @staticmethod
    def check_password(user, password):
        """
        Verify the supplied password.
        """

        return user.check_password(password)