from django.contrib.auth.mixins import UserPassesTestMixin

from .models import User


class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == User.Role.ADMIN
        )


class CustomerRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == User.Role.CUSTOMER
        )