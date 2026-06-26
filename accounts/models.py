import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    class Role(models.TextChoices):

        CUSTOMER = "CUSTOMER", "Customer"

        ADMIN = "ADMIN", "Restaurant Administrator"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    email_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email