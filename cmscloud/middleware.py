# -*- coding: utf-8 -*-
"""
Access Control Middleware
"""
from django.conf import settings
from django.http import HttpResponse
from simple_sso.sso_client.client import LoginView, Client


class AccessControlMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated() and not request.path.startswith(('/login/', '/admin/~cmscloud-api/')):
            return HttpResponse(
                '''
                <html>
                    <head>
                        <title>Login Required</title>
                    </head>
                    <body>
                        <h1>You need to log in to access this website</h1>
                        <p>Click <a href="/login/">here</a> to log in.</p>
                    </body>
                </html>
                '''
            )
        return None
