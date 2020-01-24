# Built in modules

# Django related modules
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import (
    render, 
    HttpResponseRedirect, 
    resolve_url
)

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    LogoutView
)

from django.utils.decorators import method_decorator
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)

from django.views.decorators.cache import never_cache

# Project modules
from .forms import (
    AuthenticationForm,
)

# Third party modules


__all__ = [
    "CustomLoginView",
    "CustomLogoutView"
]

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
