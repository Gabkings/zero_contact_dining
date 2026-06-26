import pytest
import uuid
from accounts.models import User

@pytest.mark.django_db
class TestUserManager:
    """
    Tests for the custom UserManager.
    """

    def test_create_user(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert user.email == "john@gmail.com"

        assert user.username == "john"

        assert user.is_active

        assert not user.is_staff

        assert not user.is_superuser



    def test_password_hashed(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert user.check_password("Password123!")


    def test_email_normalized(self):

        user = User.objects.create_user(
            username="john",
            email="John@GMAIL.COM",
            password="Password123!",
        )

        assert user.email == "John@gmail.com"


    def test_email_required(self):

        with pytest.raises(ValueError):

            User.objects.create_user(
                username="john",
                email="",
                password="Password123!",
            )


    def test_username_required(self):

        with pytest.raises(ValueError):

            User.objects.create_user(
                username="",
                email="john@gmail.com",
                password="Password123!",
            )


    def test_create_superuser(self):

        admin = User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="Password123!",
        )

        assert admin.is_superuser

        assert admin.is_staff

        assert admin.is_active


    def test_superuser_requires_staff(self):

        with pytest.raises(ValueError):

            User.objects.create_superuser(
                username="admin",
                email="admin@gmail.com",
                password="Password123!",
                is_staff=False,
            )


    def test_superuser_requires_superuser(self):

        with pytest.raises(ValueError):

            User.objects.create_superuser(
                username="admin",
                email="admin@gmail.com",
                password="Password123!",
                is_superuser=False,
            )


    def test_default_role(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert user.role == User.Role.CUSTOMER




    def test_uuid_created(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert isinstance(
            user.id,
            uuid.UUID,
        )


    def test_email_not_verified(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert not user.is_email_verified


    def test_password_not_plain_text(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        assert user.password != "Password123!"


    def test_create_multiple_users(self):

        User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        User.objects.create_user(
            username="mary",
            email="mary@gmail.com",
            password="Password123!",
        )

        assert User.objects.count() == 2