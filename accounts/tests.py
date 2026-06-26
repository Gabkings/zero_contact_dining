from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from .models import User


class UserModelTest(TestCase):

    def test_create_customer(self):

        user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="Password123!",
        )

        self.assertEqual(
            user.role,
            User.Role.CUSTOMER,
        )