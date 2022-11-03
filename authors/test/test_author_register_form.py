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
        ("email", "The e-mail must be valid."),
        ("username",
         ("Username must have at letters, numbers or one of those "
          "@.+-_. The length should be between 4 and 150 characters.")),
        ("password",
         ("Password must have a least one uppercase letter",
          "one lowecase letter and one number. The length should be",
          "at leats 8 characters.")), ("email", "The e-mail must be valid.")
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([("username", "Username"),
                           ("first_name", "first name"),
                           ("last_name", "last name"), ("email", "email"),
                           ("password", "password"),
                           ("password2", "password2")])
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

    @parameterized.expand([("username", "This field must not be empty"),
                           ("first_name", "Write your first name"),
                           ("last_name", "Write your last name"),
                           ("password", "Password must not be empty"),
                           ("password2", "Please, repeat your password"),
                           ("email", "Email is required")])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
        # self.assertIn(msg, response.context["form"].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data["username"] = "joa"
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Username must have at least 4 characters."

        # self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))

    def test_username_field_max_length_should_be_150(self):
        self.form_data["username"] = "A" * 151
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Username must have less than 150 characters."

        # self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))
