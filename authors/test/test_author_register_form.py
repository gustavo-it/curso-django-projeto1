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
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(placeholder, current_placeholder)
