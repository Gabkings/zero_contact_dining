from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

from accounts.validators import validate_phone_number

from .models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "john_doe",
            "email": "john@example.com",
            "phone_number": "+254712345678",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for field_name, field in self.fields.items():

            field.widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "placeholder": placeholders.get(field_name, ""),
                }
            )

        self.fields["phone_number"].validators.append(
            validate_phone_number
        )

    def clean_email(self):

        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"].strip()

        return phone


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="Email"
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Email Address",
                "class": "input input-bordered w-full",
            }
        )

        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Password",
                "class": "input input-bordered w-full",
            }
        )



class ProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "profile_picture",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    "class": "input input-bordered w-full"
                }
            )

            

class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })