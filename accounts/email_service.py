from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


class EmailVerificationService:

    @staticmethod
    def send_verification_email(request, user):

        token = default_token_generator.make_token(user)

        verification_url = request.build_absolute_uri(
            reverse(
                "verify_email",
                kwargs={
                    "uid": user.pk,
                    "token": token,
                },
            )
        )

        context = {
            "user": user,
            "verification_url": verification_url,
        }

        html = render_to_string(
            "emails/verify_email.html",
            context,
        )

        email = EmailMultiAlternatives(
            subject="Verify your account",
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email.attach_alternative(html, "text/html")

        email.send()