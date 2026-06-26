from django.test import TestCase

from accounts.models import User


class UserManagerTest(TestCase):

    def test_create_user(self):

        user = User.objects.create_user(
            username="john",
            email="john@gmail.com",
            password="Password123!",
        )

        self.assertTrue(user.check_password("Password123!"))

    def test_create_superuser(self):

        admin = User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="Password123!",
        )

        self.assertTrue(admin.is_superuser)

        self.assertTrue(admin.is_staff)

    def test_email_required(self):

        with self.assertRaises(ValueError):

            User.objects.create_user(
                username="john",
                email="",
                password="Password123!",
            )