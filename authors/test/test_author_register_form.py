from authors.forms import RegisterForm
from django.test import TestCase
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
