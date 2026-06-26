import pytest

from accounts.forms import (
    RegistrationForm,
    LoginForm,
    ProfileForm,
)

from accounts.tests.factories import UserFactory

@pytest.mark.django_db
class TestRegistrationForm:
    """
    Registration Form Tests
    """

    def test_valid_registration_form(self):

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


    def test_duplicate_email(self):

        UserFactory(
            email="john@gmail.com"
        )

        form = RegistrationForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john2",
                "email": "john@gmail.com",
                "phone_number": "+254712345678",
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )

        assert not form.is_valid()

        assert "email" in form.errors


    def test_invalid_phone(self):

        form = RegistrationForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john",
                "email": "john@gmail.com",
                "phone_number": "ABC123",
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )

        assert not form.is_valid()

        assert "phone_number" in form.errors


    def test_passwords_do_not_match(self):

        form = RegistrationForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john",
                "email": "john@gmail.com",
                "phone_number": "+254712345678",
                "password1": "Password123!",
                "password2": "DifferentPassword123!",
            }
        )

        assert not form.is_valid()


    def test_email_normalized(self):

        form = RegistrationForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john",
                "email": " JOHN@GMAIL.COM ",
                "phone_number": "+254712345678",
                "password1": "Password123!",
                "password2": "Password123!",
            }
        )

        assert form.is_valid()

        assert form.cleaned_data["email"] == "john@gmail.com"


    def test_placeholders_exist(self):

        form = RegistrationForm()

        assert (
            form.fields["email"]
            .widget.attrs["placeholder"]
            == "john@example.com"
        )


    def test_tailwind_classes(self):

        form = RegistrationForm()

        assert (
            "input"
            in form.fields["email"]
            .widget.attrs["class"]
        )


class TestLoginForm:

    def test_login_form_fields(self):

        form = LoginForm()

        assert "username" in form.fields

        assert "password" in form.fields


class TestProfileForm:

    def test_profile_form_fields(self):

        form = ProfileForm()

        assert "first_name" in form.fields

        assert "last_name" in form.fields

        assert "phone_number" in form.fields