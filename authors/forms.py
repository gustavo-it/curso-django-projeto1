from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

        labels = {
            "username": "Username",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "password": "password",
        }

        help_texts = {
            "email": "The e-mail must be valid."
        }

        error_messages = {
            "username": {
                "required": "This field must not be empty",
            }
        }

        widgets = {
            "first_name": forms.TextInput(attr={
                "placeholder": "type your first name here",
                "class": "input text-input"
            }),
            "password": forms.PasswordInput(attr={
                "placeholder": "Type your password here"
            })
        }
