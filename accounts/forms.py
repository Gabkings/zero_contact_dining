from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

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


class LoginForm(AuthenticationForm):
    class Meta:
        model = User

        fields = (
            "username",
            "password",
        )

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .validators import validate_phone_number


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })

    phone_number = forms.CharField(
        validators=[validate_phone_number]
    )

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
    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "Email already exists."
            )

        return email
    
    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"]

        return phone.strip()


class LoginForm(AuthenticationForm):

    username = forms.EmailField()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })



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

            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({
                "class": "input input-bordered w-full"
            })