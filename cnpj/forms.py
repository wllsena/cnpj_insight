from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """Form for registering a new user.

    Inherits from UserCreationForm and adds an email field.
    """
    email: forms.EmailField = forms.EmailField()

    class Meta:
        model: type = User
        fields: list[str] = ["username", "email", "password1", "password2"]