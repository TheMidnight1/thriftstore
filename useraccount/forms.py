from django import forms
from .models import User
from django.forms.widgets import RadioSelect
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import (
    UserChangeForm,
    PasswordChangeForm,
    UserCreationForm,
)

User = get_user_model()


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError(_("Invalid phone number. Please enter only digits."))
    if len(value) != 10:
        raise ValidationError(
            _("Invalid phone number. The phone number must have 10 digits.")
        )


def validate_first_name(value):
    if value.isdigit():
        raise ValidationError(_("Invalid . Please enter only alphabets."))



def validate_last_name(value):
    if value.isdigit():
        raise ValidationError(_("Invalid . Please enter only alphabets."))


class UserForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_phone_number],
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        validators=[EmailValidator(message="Please enter a valid email address.")],
    )
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_first_name],
    )
    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[validate_last_name],
    )

    gender_choices = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    gender = forms.ChoiceField(choices=gender_choices, widget=RadioSelect)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "username",
            "gender",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": ""}),
            "email": forms.EmailInput(
                attrs={"class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"}),
            "password": forms.PasswordInput(
                attrs={
                    "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                    
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                    
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                    
                }
            ),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "name": "username",
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(
            attrs={
                "name": "password",
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )


class EditProfileForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password field
        self.fields.pop("password")
        # Add custom classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "appearance-none block w-full py-2 px-3 leading-tight border border-gray-300 rounded focus:outline-none focus:bg-white focus:border-gray-500"
                }
            )


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("old_password", "new_password1", "new_password2")
