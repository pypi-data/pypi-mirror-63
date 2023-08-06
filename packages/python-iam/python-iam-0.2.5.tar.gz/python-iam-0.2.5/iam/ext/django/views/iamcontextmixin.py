"""Declares :class:`IAMContextMixin`."""
import os

import ioc

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView

from iam.const import MESSAGE_TOKEN_SESSION_KEY
from iam.ext.django.models import Realm


class IAMContextMixin:
    allow_signup = False
    allow_local = True
    redirect_field_name = LoginView.redirect_field_name
    principals = {
        'username': _('username'),
        'email': _('email address'),
        'phonenumber': _('phonenumber')
    }
    jwt = ioc.class_property('JWTService')

    #: Specifies the realm to which the :term:`Subject` will login.
    realm = settings.IAM_REALM

    #: Specifies the splash image.
    splash_image = settings.IAM_IMAGE_SPLASH

    #: Indicates if public (i.e. from the internet) :term:`Subjects` may
    #: login.
    allow_public = False

    def get_enabled_principals(self):
        """Returns the principal kinds that are enabled."""
        return list(settings.IAM_ACCOUNT_PRINCIPALS)

    def get_state_param(self):
        self.request.session[MESSAGE_TOKEN_SESSION_KEY] = token =\
            bytes.hex(os.urandom(16))
        return bytes.decode(self.jwt.encrypt({
            'rlm': self.realm,
            'token': token
        }))

    def get_context_data(self, *args, **kwargs):
        """Return the template context dictionary to use when rendering
        templates.
        """
        ctx = super().get_context_data(*args, **kwargs)
        ctx['iam_state_param'] = self.get_state_param()
        ctx['iam_portal_name']  = "Unimatrix One"
        ctx['iam_url_namespace'] = settings.IAM_URL_NAMESPACE
        ctx['iam_urls'] = {
            'forms': {
                'names': f'{settings.IAM_URL_NAMESPACE}:forms:names',
                'terms': f'{settings.IAM_URL_NAMESPACE}:forms:terms',
            },
            'login': f'{settings.IAM_URL_NAMESPACE}:login',
            'login_token': f'{settings.IAM_URL_NAMESPACE}:login.token',
            'logout': f'{settings.IAM_URL_NAMESPACE}:logout',
            'register': f'{settings.IAM_URL_NAMESPACE}:register',
            'resetcredentials': f'{settings.IAM_URL_NAMESPACE}:resetcredentials',
        }
        ctx['social_auth_begin_url'] = f'{settings.SOCIAL_AUTH_URL_NAMESPACE}:begin'
        ctx.update({
            'iam_allow_signup': self.allow_signup,
            'iam_enable_local': self.allow_local\
                and bool(settings.IAM_ACCOUNT_PRINCIPALS),
            'iam_enable_magic_link': settings.IAM_ENABLE_MAGIC_LINK,
            'iam_enable_password_reset': settings.IAM_ENABLE_PASSWORD_RESET,
            'iam_image_logo': settings.IAM_IMAGE_LOGO,
            'iam_principals_placeholder': self.get_principal_placeholder(),
            'iam_public_realm': self.allow_public,
            'iam_redirect_field_name': self.redirect_field_name,
            'iam_require_username': settings.IAM_REQUIRE_USERNAME,
        })

        capabilities = ctx['iam_capabilities'] = []

        if self.splash_image is not None:
            ctx['iam_image_splash'] = self.splash_image

        # Determine login capabilities from settings and realm
        realm = Realm.objects.get(name=self.realm)
        for provider in realm.getssoproviders():
            capabilities.append(f'login:{provider}')

        # Add the next URL to the template context to external providers
        # can also login and redirect to the appropriate location.
        #raise Exception(self.request.GET['next'])

        return ctx

    def get_principal_placeholder(self):
        """Return the placeholder for the principal input field based on the
        configured principal types.
        """
        principals = [str(self.principals[x])
            for x in self.get_enabled_principals()]
        placeholder = ''
        if len(principals) == 1:
            placeholder = principals[0]
        else:
            placeholder += str.join(', ', principals[:-1])
            placeholder += ' ' + str(_('or')) + ' '
            placeholder += principals[-1]
        return str.title(placeholder[0]) + placeholder[1:]

    def get_realm(self):
        """Returns the :term:`Realm` for this controller."""
        return self.realm
