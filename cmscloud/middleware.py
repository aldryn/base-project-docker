# -*- coding: utf-8 -*-
"""
Access Control Middleware
"""
import datetime
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core import signing
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from cmscloud.sso import ALDRYN_USER_SESSION_KEY

import logging
logger = logging.getLogger('aldryn')


DEMO_ACCESS_TOKEN_KEY_NAME = getattr(settings, 'DEMO_ACCESS_TOKEN_KEY_NAME', None)
DEMO_ACCESS_SECRET_STRING = getattr(settings, 'DEMO_ACCESS_SECRET_STRING', None)
DEMO_ACCESS_TIMEOUT_KEY_NAME = '{}-timeout_at'.format(DEMO_ACCESS_TOKEN_KEY_NAME)
DEMO_ACCESS_TIMEOUT_IN_S_KEY_NAME = getattr(settings, 'DEMO_ACCESS_TIMEOUT_IN_S_KEY_NAME', 'demo_timeout_s')
DEMO_MODE_ACTIVE = getattr(settings, 'DEMO_MODE_ACTIVE', None)


class DemoAccessControlMiddleware(object):
    def process_request(self, request):
        if not DEMO_MODE_ACTIVE:
            return

        if self.check_signature(request):
            self.init_user(request)
            return HttpResponseRedirect('/')

        if self.demo_expired(request):
            return TemplateResponse(request, 'cmscloud/demo_expired.html')

    def demo_expired(self, request):
        """
        Checks whether the demo has expired. Not having a timeout session variable is considered
        as timed out.
        Warning: side-effects! saves the timeout in s on the request for usage in the frontend.
        """
        timeout_at = request.session.get(DEMO_ACCESS_TIMEOUT_KEY_NAME, None)
        if timeout_at:
            timeout_at = datetime.datetime(*timeout_at[0:7])
            timeout_in = timeout_at - datetime.datetime.now()
            if timeout_in <= datetime.timedelta(0):
                timeout_in = datetime.timedelta(0)
            logger.info('demo: timeout at {} ({} left)'.format(
                timeout_at,
                timeout_in,
            ))
            setattr(request, DEMO_ACCESS_TIMEOUT_IN_S_KEY_NAME, int(timeout_in.total_seconds()))
            return timeout_at < datetime.datetime.now()
        else:
            logger.info('demo: no timeout session variable set')
            setattr(request, DEMO_ACCESS_TIMEOUT_IN_S_KEY_NAME, 0)
            return True

    def check_signature(self, request):
        """
        Checks whether the there is a signature in the url and whether it is valid.
        Warning: side-effects! saves the timeout in the session if the singature is valid.
        """
        demo_access_token = request.GET.get(DEMO_ACCESS_TOKEN_KEY_NAME, None)
        if not demo_access_token:
            return None

        signer = signing.Signer(DEMO_ACCESS_SECRET_STRING)
        try:
            timeout = signer.unsign(demo_access_token)
            if request.session.get(DEMO_ACCESS_TIMEOUT_KEY_NAME, None) is None:
                # only re-set the timeout if it is not set already. Otherwise
                # someone can reload the page with the original get parameter to extend
                # the demo. In practice it would be re-deployed short thereafter anyway...
                # but we don't want people to feel the system is easy to hack.
                # TODO: a cleaner solution would be to sign the timestamp when the demo should
                #       expire. But that would introduce troubles with timezones and exact time
                #       matching between servers.
                timeout = datetime.timedelta(seconds=int(timeout))
                timeout_datetime = datetime.datetime.now() + timeout
                request.session[DEMO_ACCESS_TIMEOUT_KEY_NAME] = tuple((timeout_datetime).timetuple())
                request.session.save()
                return True
            else:
                return None
        except (signing.BadSignature, ValueError) as e:
            logger.warning('invalid demo signature {}'.format(e))
            return False

    def init_user(self, request):
        """
        Create and login a demo user.
        """
        try:
            user = User.objects.get(username='aldryn demo')
        except User.DoesNotExist:
            user = User(username='aldryn demo')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        user.backend = "%s.%s" % (ModelBackend.__module__, ModelBackend.__name__)
        login(request, user)


class AccessControlMiddleware(object):
    def process_request(self, request):
        demo_access_control = DemoAccessControlMiddleware().process_request(request=request)
        if demo_access_control is not None:
            return demo_access_control

        if request.user.is_authenticated():
            # the user is already logged in
            return None
        if request.path.startswith(('/login/', '/admin/~cmscloud-api/',
                                    '/trigger-sync-changed-files/', '/sitemap.xml')):
            # internal api call, skipping the authentication check
            return None
        if request.session.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME):
            # the user accessed the website with the sharing token,
            # skipping the authentication check
            return None

        # check if the user is using the "view only sharing url"
        token = request.GET.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME, None)
        if settings.SHARING_VIEW_ONLY_SECRET_TOKEN == token:
            request.session[settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME] = token
            return HttpResponseRedirect('/')

        return TemplateResponse(request, 'cmscloud/login_screen.html')


# copied from django 1.7a2: https://github.com/django/django/blob/1.7a2/django/contrib/sites/middleware.py
from django.contrib.sites.models import Site


class CurrentSiteMiddleware(object):
    """
    Middleware that sets `site` attribute to request object.
    """

    def process_request(self, request):
        request.site = Site.objects.get_current()


class AldrynUserMiddleware(object):
    """
    Middleware that protects Aldryn Cloud users from hijacking their accounts
    by previously created django users with the same email address or username.
    """

    def process_request(self, request):
        user = request.user
        if ALDRYN_USER_SESSION_KEY in request.session:
            # properly logged in Aldryn Cloud user
            return None
        elif hasattr(user, 'aldryn_cloud_account'):
            # this is an Aldryn Cloud account that wasn't logged in with a sso,
            # deactivating its session.
            user.set_unusable_password()  # sso doesn't require local passwords
            user.save()
            logout(request)
            return HttpResponseRedirect('/')
