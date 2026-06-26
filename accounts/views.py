from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View

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

    template_name = "accounts/login.html"

    authentication_form = LoginForm

    redirect_authenticated_user = True

    def form_valid(self, form):

        messages.success(
            self.request,
            "Welcome back!"
        )

        return super().form_valid(form)


class UserLogoutView(LogoutView):

    next_page = reverse_lazy("login")


class RegisterView(CreateView):

    form_class = RegistrationForm

    template_name = "accounts/register.html"

    success_url = reverse_lazy("login")

    def form_valid(self, form):

        validated_data = form.cleaned_data.copy()

        validated_data["password"] = validated_data.pop(
            "password1"
        )

        validated_data.pop(
            "password2",
            None,
        )

        user = AuthenticationService.register_user(
            validated_data
        )

        token = EmailVerificationService.generate_token(
            user
        )

        verification_url = self.request.build_absolute_uri(
            reverse_lazy(
                "verify_email",
                kwargs={
                    "uid": user.pk,
                    "token": token,
                },
            )
        )

        EmailVerificationService.send_verification_email(
            user,
            verification_url,
        )

        messages.success(
            self.request,
            "Account created successfully. Please verify your email."
        )

        return redirect(
            self.success_url
        )


class ProfileView(LoginRequiredMixin, UpdateView):

    model = User

    form_class = ProfileForm

    template_name = "accounts/profile.html"

    success_url = reverse_lazy("profile")

    def get_object(self):

        return self.request.user

    def form_valid(self, form):

        ProfileService.update_profile(

            self.request.user,

            form.cleaned_data,

        )

        messages.success(

            self.request,

            "Profile updated successfully.",

        )

        return redirect(self.success_url)


class ChangePasswordView(LoginRequiredMixin, View):

    template_name = "accounts/change_password.html"

    def get(self, request):

        form = CustomPasswordChangeForm(
            request.user
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request):

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
                "Password updated."
            )

            return redirect(
                "profile"
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )


class VerifyEmailView(View):

    def get(
        self,
        request,
        uid,
        token,
    ):

        user = get_object_or_404(
            User,
            pk=uid,
        )

        if EmailVerificationService.verify_token(
            user,
            token,
        ):

            EmailVerificationService.activate_user(
                user
            )

            messages.success(
                request,
                "Email verified successfully."
            )

            return redirect("login")

        messages.error(
            request,
            "Invalid verification link."
        )

        return redirect("register")