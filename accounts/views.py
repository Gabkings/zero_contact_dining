from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .forms import CustomPasswordChangeForm
from .services import AuthenticationService
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LogoutView


def register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = AuthenticationService.register_user(form)

            AuthenticationService.login_user(request, user)
            messages.success(request, "Your account has been created successfully.")

            return redirect("dashboard")

    else:
        messages.error(request, "Failed to create account.")
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )



class UserLoginView(LoginView):

    template_name = "accounts/login.html"

    authentication_form = LoginForm

    redirect_authenticated_user = True




class UserLogoutView(LogoutView):

    next_page = "login"



@login_required
def profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():

            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

    else:
        messages.error(request, "Failed to update profile.")
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
        },
    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "Password updated successfully."
            )

            return redirect("profile")

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form
        },
    )


def verify_email(request, uid, token):

    user = get_object_or_404(
        User,
        pk=uid,
    )

    if default_token_generator.check_token(user, token):

        user.is_active = True

        user.is_email_verified = True

        user.save()

        return redirect("login")

    return redirect("register")