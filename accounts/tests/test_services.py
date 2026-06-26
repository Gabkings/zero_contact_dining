import pytest
from unittest.mock import patch

from accounts.forms import RegistrationForm
from accounts.models import User
from accounts.services import (
    AuthenticationService,
    ProfileService,
    PasswordService,
    EmailVerificationService,
)

from accounts.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


##############################################################
# Authentication Service
##############################################################

class TestAuthenticationService:

    def test_register_user(self):

        form = RegistrationForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john",
                "email": "john@gmail.com",
                "phone_number": "+254712345678",
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )

        assert form.is_valid()

        validated_data = form.cleaned_data.copy()

        validated_data["password"] = validated_data.pop("password1")
        validated_data.pop("password2", None)

        user = AuthenticationService.register_user(
            validated_data
        )

        assert isinstance(user, User)

        assert user.email == "john@gmail.com"

        assert user.role == User.Role.CUSTOMER

        assert user.is_active is False

        assert user.check_password("Password123!")


##############################################################
# Profile Service
##############################################################

class TestProfileService:

    def test_update_profile(self):

        user = UserFactory()

        ProfileService.update_profile(
            user,
            {
                "first_name": "Gabriel",
                "last_name": "Gitonga",
                "phone_number": "+254700123456",
            },
        )

        user.refresh_from_db()

        assert user.first_name == "Gabriel"

        assert user.last_name == "Gitonga"

        assert user.phone_number == "+254700123456"


##############################################################
# Password Service
##############################################################

class TestPasswordService:

    def test_change_password(self):

        user = UserFactory(password="Password123!")

        PasswordService.change_password(
            user,
            "NewPassword123!",
        )

        user.refresh_from_db()

        assert user.check_password("NewPassword123!")

    def test_check_password(self):

        user = UserFactory(password="Password123!")

        assert PasswordService.check_password(
            user,
            "Password123!",
        )

        assert not PasswordService.check_password(
            user,
            "WrongPassword",
        )


##############################################################
# Email Verification Service
##############################################################

class TestEmailVerificationService:

    def test_generate_token(self):

        user = UserFactory()

        token = EmailVerificationService.generate_token(
            user
        )

        assert token is not None

    def test_verify_token(self):

        user = UserFactory()

        token = EmailVerificationService.generate_token(
            user
        )

        assert EmailVerificationService.verify_token(
            user,
            token,
        )

    def test_invalid_token(self):

        user = UserFactory()

        assert not EmailVerificationService.verify_token(
            user,
            "invalid-token",
        )

    def test_activate_user(self):

        user = UserFactory(
            is_active=False,
            is_email_verified=False,
        )

        EmailVerificationService.activate_user(
            user
        )

        user.refresh_from_db()

        assert user.is_active

        assert user.is_email_verified

    @patch("accounts.services.email.send_mail")
    def test_send_verification_email(
        self,
        mock_send_mail,
    ):

        user = UserFactory()

        EmailVerificationService.send_verification_email(
            user,
            "http://localhost/verify",
        )

        mock_send_mail.assert_called_once()