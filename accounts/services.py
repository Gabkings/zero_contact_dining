from .models import User


def register_customer(form):

    user = form.save(commit=False)

    user.role = User.Role.CUSTOMER

    user.save()

    return user

