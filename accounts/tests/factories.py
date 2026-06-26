import factory

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")

    last_name = factory.Faker("last_name")

    username = factory.Sequence(
        lambda n: f"user{n}"
    )

    email = factory.Sequence(
        lambda n: f"user{n}@gmail.com"
    )

    phone_number = "0712345678"

    is_active = True

    role = User.Role.CUSTOMER

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        password = extracted or "Password123!"
        obj.set_password(password)

        if create:
            obj.save()



class AdminFactory(UserFactory):

    role = User.Role.ADMIN

    is_staff = True

    is_superuser = True