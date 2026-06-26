from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

from .models import User


def admin_required(view_func):
    """
    Allows access only to restaurant administrators.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        ):
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "You do not have permission to access this page."
        )

        return redirect("dashboard")

    return wrapper


def customer_required(view_func):
    """
    Allows access only to customers.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if (
            request.user.is_authenticated
            and request.user.role == User.Role.CUSTOMER
        ):
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Access denied."
        )

        return redirect("dashboard")

    return wrapper