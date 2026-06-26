from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    UserLoginView,
    UserLogoutView,
    register,
    profile,
    change_password,
    verify_email,
)

urlpatterns = [

    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),

    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "profile/",
        profile,
        name="profile",
    ),

    path(
        "change-password/",
        change_password,
        name="change_password",
    ),

    path(
        "verify/<uuid:uid>/<str:token>/",
        verify_email,
        name="verify_email",
    ),

    # Password Reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="emails/password_reset_email.html",
            success_url="/accounts/password-reset/done/",
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/accounts/reset-complete/",
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]