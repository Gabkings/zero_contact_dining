from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


class EmailVerificationService:
    """
    Handles email verification operations.
    """

    @staticmethod
    def generate_token(user):
        return default_token_generator.make_token(user)

    @staticmethod
    def verify_token(user, token):
        return default_token_generator.check_token(user, token)

    @staticmethod
    def activate_user(user):
        user.is_active = True
        user.is_email_verified = True

        user.save(update_fields=["is_active", "is_email_verified"])

        return user

    @staticmethod
    def send_verification_email(user, verification_url):
        send_mail(
            subject="Verify your account",
            message=(
                "Welcome to Zero Contact Dining.\n\n"
                f"Please verify your account by visiting:\n{verification_url}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )