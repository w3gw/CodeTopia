# Built in modules
import unicodedata

# Django related modules
from django import forms

# Project modules
from django.template import loader

from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _

# Third party modules


UserModel = get_user_model()

__all__ = [
    "AuthenticationForm"
    ]

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        """Return HTML form attribute set for UserName field from CharField"""
        return {
            **super().widget_attrs(widget),
            "autofocus": True
            # add extra HTML attributes for UsernameField
        }


class AuthenticationForm(forms.Form):
    """AuthenticationForm: Form authenticating user using username and password"""

    # Create Fields for The User Authentication
    username = UsernameField(label=_("Username"), strip=False )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            # add extra HTML attributes for password
        }),
    )

    # Error Messages: error message to be rendered incase of form.is_valid() returns False
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
            The 'request' parameter is set for custom auth use by subclasses.
            The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)

        # Set maximum_length property to the UerNameField
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length

        # set HTML attribute maxlength to max_length retrieved either from the UserModel or Default
        self.fields['username'].widget.attrs['maxlength'] = username_max_length

        # if the username field has no label
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        """ return clean data by authenticating the cridentials"""

        if self.cleaned_data.get('username') is not None and self.cleaned_data.get('password'):
            # authenticate will return user instance is the user exists and authenticated
            self.user_cache = authenticate(
                    request=self.request,
                    username=self.cleaned_data.get('username'), 
                    password=self.cleaned_data.get('password')
                )
            if self.user_cache is None:
                # if there is no user with the cridentials get_invalid_login_error()
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        # if authenticate returns a user
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method raises raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            # if the user is not active the raise inactive error_message
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
