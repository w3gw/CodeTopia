
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from django.core import mail

from django.contrib.auth.models import User

from account.views import *
from account.forms import *
from account.urls import *

from django import forms

class TestAuthenticationForm(TestCase):
    """Test AuthenticationForm: used for loging in a user"""
    def setUp(self):
        self.user1_cridentials = {
            "username": "test_user_1", 
            "email": "test_email_1@gmail.com", 
            "password": "test_user_1_password"
        }
        self.user2_cridentials = {
            "username": "test_user_2", 
            "email": "test_email_2@gmail.com", 
            "password": "test_user_2_password"
        }

        # create a user from the above user data
        self.user = User.objects.create_user(
            username=self.user1_cridentials["username"],
            email=self.user1_cridentials["email"],
            password=self.user1_cridentials["password"])

    def test_clean_email_valid(self):
        """test AuthenticationForm clean_email using valid user cridentials and data"""
        form = AuthenticationForm({
            "username": self.user1_cridentials.get("password"),
            "password": self.user1_cridentials.get("password")
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user1_cridentials["username"], form.clean_username())
'''
    def test_clean_email_invalid1(self):
        """test AuthenticationForm clean_email using invalid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': 'a@a.com',
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('email' in form.errors)
        email_error = form.errors["email"]
        self.assertEqual('invalid email', email_error[0])

    def test_clean_email_invalid2(self):
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.created_user.email,
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('email' in form.errors)
        email_error = form.errors["email"]
        self.assertEqual('the email has already exists. DONT TRY THIS AGAIN!!!', email_error[0])

    def test_clean_username_valid(self):
        """test AuthenticationForm clean_username using valid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user2_cridentials["username"], form.clean_username())

    def test_clean_username_invalid(self):
        """test AuthenticationForm clean_username using invalid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user1_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('username' in form.errors)
        email_error = form.errors["username"]
        self.assertEqual('A user with that username already exists.', email_error[0])

    def test_clean_password_valid(self):
        """test AuthenticationForm clean_password2 using valid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user2_cridentials["password"], form.clean_password2())

    def test_clean_password_invalid1(self):
        """test AuthenticationForm clean_password2 using invalid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]+str(45)
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('password2' in form.errors)
        email_error = form.errors["password2"]
        self.assertEqual('The two password fields didn’t match.', email_error[0])

    def test_clean_password_invalid2(self):
        """test AuthenticationForm clean_password2 using invalid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': "abc",
            'password2': "abc"
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('password2' in form.errors)
        email_error = form.errors["password2"]
        self.assertEqual('This password is too short. It must contain at least 8 characters.', email_error[0])

    def test_clean_password_invalid3(self):
        """test AuthenticationForm clean_password2 using invalid user cridentials and data"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': "qwertyui",
            'password2': "qwertyui"
        })
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('password2' in form.errors)

        # use the following test for testing for via request reponse to test form error rendering
        # self.assertFormError(
        #     response=response, 
        #     form=AuthenticationForm, 
        #     field=password, 
        #     errors="This password is too common.", 
        #     msg_prefix='')

        email_error = form.errors["password2"]
        self.assertEqual('This password is too common.', email_error[0])

    def test_AuthenticationForm_save(self):
        """test by creating a user by providing valid user data and cridentails"""
        form = AuthenticationForm ({
            'username': self.user2_cridentials["username"],
            'email': self.user2_cridentials["email"],
            'password1': self.user2_cridentials["password"],
            'password2': self.user2_cridentials["password"]
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user2_cridentials["username"], User.objects.get(username=self.user2_cridentials["username"]).username)'''