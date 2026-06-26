from django.contrib.auth import login
from django.db import transaction

from .models import User


class AuthenticationService:

    @staticmethod
    @transaction.atomic
    def register_user(form):
        """
        Creates a new customer account.
        """

        user = form.save(commit=False)

        user.role = User.Role.CUSTOMER

        user.is_active = False

        user.save()

        return user

    @staticmethod
    def login_user(request, user):
        login(request, user)