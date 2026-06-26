from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import RegistrationForm, LoginForm
from .services import register_customer


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = "login"


def register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = register_customer(form)

            login(request, user)

            return redirect("dashboard")

    else:

        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )