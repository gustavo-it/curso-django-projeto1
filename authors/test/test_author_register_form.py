from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ("username", "Your username"),
        ("first_name", "Ex: Maria"),
        ("last_name", "Ex: Doe"),
        ("password", "Type your password"),
        ("password2", "Repeat your password"),
        ("email", "Your email"),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ("email", "The e-mail must be valid.")
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ("username", "Username"),
        ("first_name", "first_name"),
        ("last_name", "last_name"),
        ("email", "email"),
        ("password", "password"),
        ("password2", "password2")
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationtEST(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@anymail.com",
            "password": "Str0ngP@ssword1",
            "password2": "Str0ngP@ssword2",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ("username", "This field must not be empty"),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
