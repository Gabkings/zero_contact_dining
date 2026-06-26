import factory

from accounts.models import User


class CustomerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = "John"

    last_name = "Doe"

    username = factory.Sequence(
        lambda n: f"customer{n}"
    )

    email = factory.Sequence(
        lambda n: f"customer{n}@gmail.com"
    )

    phone_number = "0712345678"

    role = User.Role.CUSTOMER

    is_active = True


class AdminFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = "Restaurant"

    last_name = "Admin"

    username = factory.Sequence(
        lambda n: f"admin{n}"
    )

    email = factory.Sequence(
        lambda n: f"admin{n}@gmail.com"
    )

    role = User.Role.ADMIN

    is_active = True