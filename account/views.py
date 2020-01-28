# Built in modules

# Django related modules
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import (
    render, 
    HttpResponseRedirect, 
    resolve_url
)
from django.urls import (
    reverse,
    reverse_lazy
)

from django.template import loader

from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)

from django.utils import timezone

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from django.utils.translation import gettext, gettext_lazy as _
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)

from django.views.decorators.cache import never_cache

from django.views.generic.base import View
from django.views.generic.edit import FormView

from django.contrib import messages

# Project modules
from .forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
    PasswordChangeForm
)

# Third party modules


__all__ = [
    "CustomLoginView",
    "CustomLogoutView",
    "CustomPasswordResetView",
    "CustomPasswordResetDoneView",
    "CustomPasswordResetConfirmView",
    "CustomPasswordResetCompleteView",
    "CreateUserView",
    "UserDashboard",
    "UserPasswordChangeView"
]

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CreateUserView(View):
    """Class for creating user with no priviledges"""

    template_name = "account/create_account.html"

    form_class = UserCreationForm
    title = _('CodeTopia | Create Account')
    extra_context = None

    # Error messages for the view
    error_messages = {
        "already_have_account": _("You already have an account and can not create another account.")
    }
    # Success messages for the view
    success_messages = {
        "account_created": _("Congradulation %s you have created  an account succesfully.")
    }

    def get_context_data(self, *args, **kwargs):
        """Return all context data by collecting it."""
        current_site = get_current_site(self.request)
        context = {
            "site": current_site,
            "site_name": current_site.name,
            "title": self.title
        }
        context.update(**(self.extra_context or {}))
        return context

    def get_form_class(self, *args, **kwargs):
        """Return the instance of the for class to be used."""
        return self.form_class(*args)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(request=self.request, message=self.error_messages.get("already_have_account"))
            return HttpResponseRedirect(reverse("core:homepage"))

        self.extra_context = {
            "form": self.get_form_class()
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def post(self, *args, **kwargs):
        form = self.get_form_class(self.request.POST)
        if form.is_valid():
            user_cache = form.save()
            messages.success(
                request=self.request, 
                message=self.success_messages.get("account_created") % user_cache.username 
            )

            return HttpResponseRedirect(reverse(viewname="account:user_login"))

        # If the form is invalid return the form with error messages
        self.extra_context = {
            **self.get_context_data(),
            "form": form
        }
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "account/login.html"

    title = _("CodeTopia | Login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            # add extra hidden field with the redirect URL after login
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

    def get_redirect_url(self):
        """Return URL to redirect the logged in user if the URL is safe."""

        redirect_to = self.request.POST.get(
            # get redirect url from the hidden next field
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def form_valid(self, form):
        """If the user cridentials rae valid log in the user using login() method."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return redirect URL from redirect_field or return from settings.LOGIN_REDIRECT_URL."""

        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


class CustomLogoutView(LogoutView):
    """Class for loging authenticated out"""
    extra_context = None
    next_page = None

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'site': current_site,
            'site_name': current_site.name,
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'account/pwd_reset/password_reset_email.html'
    subject_template_name = 'account/pwd_reset/password_reset_subject.txt'
    # extra_email_context
    html_email_template_name = 'account/pwd_reset/password_reset_html_template.html'

    success_url = reverse_lazy('account:user_password_reset_done')
    title = _('CodeTopia | Request Password Reset')
    form_class = PasswordResetForm
    template_name = "account/pwd_reset/password_reset.html"
    extra_context = {
        "expiration_date": timezone.now()
    }

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/pwd_reset/password_reset_done.html"
    title = _('CodeTopia | Password Reset Sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy("account:user_password_reset_complete")

    title = _('CodeTopia | Enter New Password')
    template_name = "account/pwd_reset/password_reset_confirm.html"
    extra_context = {
        # add extra context to be passed
    }

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/pwd_reset/password_reset_complete.html"
    title = _('CodeTopia | Password Reset Complete')

    extra_context = None

    def get_context_data(self, **kwargs):
        # the super method is calling PasswordContextMixin from PasswordResetCompleteView
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


class UserDashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    UserDashboard where only the user can access
    """
    template_name = "account/dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = {
            "title": _("CodeTopia | %s"% self.kwargs.get("username"))
        }
        return context

    def test_func(self):
        """
        Test the request sender if he has permission to access the page
        """
        return self.request.user.username == self.kwargs.get("username")

    def get_test_func(self):
        """
        Call all tests that has to be passed to access the page
        """
        return self.test_func

    def get(self, *args, **kwargs):
        self.get_context_data().update({

        })
        return render(request=self.request, template_name=self.template_name, context=self.get_context_data())


class UserPasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = "account/dashboard/change_password.html"
    title = _("CodeTopia | Chnage Password")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)