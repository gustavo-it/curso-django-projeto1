from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing_attr} {attr_new_val}".strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Your username")
        add_placeholder(self.fields["email"], "Your email")
        add_placeholder(self.fields["first_name"], "Ex: Maria")
        add_placeholder(self.fields["last_name"], "Ex: Doe")

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            "placeholder": "Repeat your password",
        }
    ))

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
            "first_name": forms.TextInput(attrs={
                "placeholder": "type your first name here",
                "class": "input text-input"
            }),
            "password": forms.PasswordInput(attrs={
                "placeholder": "Type your password here"
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get("password")

        if self.cleaned_data.get("first_name") in data:
            raise ValidationError(
                "Não digite o seu nome na senha",
                code="invalid"
            )

        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')

        if 'John Doe' in data:
            raise ValidationError(
                "Não digite %(value)s  no campo last name",
                code='invalid',
                params={"value": "'John Doe"}
            )

        return data
