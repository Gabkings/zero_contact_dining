import uuid

import pytest
from django.db import IntegrityError
from django.utils import timezone

from accounts.models import User
from accounts.tests.factories import (
    UserFactory,
    AdminFactory,
)



@pytest.mark.django_db
class TestUserModel:
    """
    Tests for the custom User model.
    """
    def test_create_customer(self):

        user = UserFactory()

        assert user.role == User.Role.CUSTOMER

        assert user.is_active


    def test_create_admin(self):

        admin = AdminFactory()

        assert admin.role == User.Role.ADMIN

        assert admin.is_staff

        assert admin.is_superuser

    def test_uuid_generated(self):

        user = UserFactory()

        assert user.id is not None
        assert isinstance(user.id,uuid.UUID)


    def test_email_unique(self):

        UserFactory(
            email="john@gmail.com"
        )

        with pytest.raises(IntegrityError):

            UserFactory(
                email="john@gmail.com"
            )

    def test_default_role(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert user.role == User.Role.CUSTOMER


    def test_phone_number(self):

        user = UserFactory(
            phone_number="0712345678"
        )

        assert user.phone_number == "0712345678"

    def test_email_not_verified_by_default(self):

        user = UserFactory()

        assert user.is_email_verified is False


    def test_created_timestamp(self):

        user = UserFactory()

        assert user.created_at <= timezone.now()


    def test_updated_timestamp(self):

        user = UserFactory()

        old = user.updated_at

        user.first_name = "Updated"

        user.save()

        user.refresh_from_db()

        assert user.updated_at >= old


    def test_full_name_property(self):

        user = UserFactory(
            first_name="John",
            last_name="Doe",
        )

        assert user.full_name == "John Doe"


    def test_is_customer_property(self):

        user = UserFactory()

        assert user.is_customer


    def test_is_admin_property(self):

        admin = AdminFactory()

        assert admin.is_restaurant_admin



    def test_email_required(self):

        with pytest.raises(ValueError):

            User.objects.create_user(
                username="john",
                email="",
                password="Password123!",
            )


    def test_password_hashed(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert user.password != "Password123!"

        assert user.check_password(
            "Password123!"
        )


    def test_username_field(self):

        assert User.USERNAME_FIELD == "email"


    def test_required_fields(self):

        assert "username" in User.REQUIRED_FIELDS

    def test_profile_picture_optional(self):

        user = UserFactory()

        assert not user.profile_picture