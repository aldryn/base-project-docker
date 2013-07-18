# -*- coding: utf-8 -*-
"""
Access Control Middleware
"""
from django.conf import settings
from simple_sso.sso_client.client import LoginView, Client


class AccessControlMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated() and not request.path.startswith(('/login/', '/admin/~cmscloud-api/')):
            view = LoginView.as_view(client=Client.from_dsn(settings.SSO_DSN))
            return view(request)
        return None
