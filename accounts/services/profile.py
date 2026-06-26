from django.db import transaction


class ProfileService:
    """
    Handles profile-related operations.
    """

    @staticmethod
    @transaction.atomic
    def update_profile(user, validated_data):
        """
        Update user profile information.
        """

        for field, value in validated_data.items():
            setattr(user, field, value)

        user.save()

        return user

    @staticmethod
    def upload_profile_picture(user, image):
        """
        Upload or replace the profile picture.
        """

        user.profile_picture = image
        user.save(update_fields=["profile_picture"])

        return user