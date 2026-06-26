from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    RegistrationForm,
    LoginForm,
    ProfileForm,
    CustomPasswordChangeForm,
)
from .models import User
from .services import (
    AuthenticationService,
    ProfileService,
    PasswordService,
    EmailVerificationService,
)


class UserLoginView(LoginView):
    """
    Handles user login.
    """

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        Optional success message.
        """
        messages.success(self.request, "Welcome back!")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """
    Handles user logout.
    """

    next_page = "login"


def register(request):
    """
    Register a new customer account.
    """

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            validated_data = form.cleaned_data.copy()

            validated_data["password"] = validated_data.pop("password1")
            validated_data.pop("password2")

            user = AuthenticationService.register_user(validated_data)

            token = EmailVerificationService.generate_token(user)

            verification_url = request.build_absolute_uri(
                f"/accounts/verify/{user.pk}/{token}/"
            )

            EmailVerificationService.send_verification_email(
                user=user,
                verification_url=verification_url,
            )

            messages.success(
                request,
                "Registration successful. Please verify your email before logging in.",
            )

            return redirect("login")

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile(request):
    """
    View and update user profile.
    """

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():

            ProfileService.update_profile(
                request.user,
                form.cleaned_data,
            )

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect("profile")

    else:

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
    """
    Change user password.
    """

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            PasswordService.change_password(
                request.user,
                form.cleaned_data["new_password1"],
            )

            update_session_auth_hash(
                request,
                request.user,
            )

            messages.success(
                request,
                "Password changed successfully.",
            )

            return redirect("profile")

    else:

        form = CustomPasswordChangeForm(request.user)

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form,
        },
    )


def verify_email(request, uid, token):
    """
    Verify user email address.
    """

    user = get_object_or_404(
        User,
        pk=uid,
    )

    if EmailVerificationService.verify_token(
        user,
        token,
    ):

        EmailVerificationService.activate_user(user)

        messages.success(
            request,
            "Your email has been verified successfully. You can now log in.",
        )

        return redirect("login")

    messages.error(
        request,
        "Verification link is invalid or has expired.",
    )

    return redirect("register")