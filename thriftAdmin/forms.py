from django import forms
from useraccount.models import User
from django.contrib.auth.forms import AuthenticationForm


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