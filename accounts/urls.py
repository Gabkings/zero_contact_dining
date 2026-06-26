from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    ChangePasswordView,
    ProfileView,
    RegisterView,
    UserLoginView,
    UserLogoutView,
    VerifyEmailView,
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
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),

    path(
        "verify/<uuid:uid>/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
]