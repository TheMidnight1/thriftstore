from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User
from .forms import UserForm

class UserFormTest(TestCase):
    def test_valid_user_form(self):
        # Test data for a valid user form
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "username": "johndoe",
            "gender": "male",
            "password1": "mypassword123",
            "password2": "mypassword123",
        }

        form = UserForm(data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_user_form(self):
        # Test data for an invalid user form with invalid phone number
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "abc",  # Invalid phone number with non-digits
            "username": "johndoe",
            "gender": "male",
            "password1": "mypassword123",
            "password2": "mypassword123",
        }

        form = UserForm(data)

        # Assert that the form is invalid
        self.assertFalse(form.is_valid())
        # Assert that the phone_number field has the appropriate error message
        self.assertEqual(
            form.errors["phone_number"][0], "Invalid phone number. Please enter only digits."
        )
