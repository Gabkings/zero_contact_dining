from django.contrib.auth import login, logout
from django.db import transaction

from accounts.models import User


class AuthenticationService:
    """
    Handles authentication-related business logic.
    """

    @staticmethod
    @transaction.atomic
    def register_user(validated_data):
        """
        Register a new customer.
        """

        password = validated_data.pop("password")

        user = User(**validated_data)

        user.role = User.Role.CUSTOMER

        user.is_active = False

        user.set_password(password)

        user.save()

        return user

    @staticmethod
    def login_user(request, user):
        login(request, user)

    @staticmethod
    def logout_user(request):
        logout(request)