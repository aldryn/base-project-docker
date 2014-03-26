# -*- coding: utf-8 -*-
from django.conf import settings
from simple_sso.sso_client.client import Client, AuthenticateView


class QuickerExpirationAuthenticateView(AuthenticateView):
    def get(self, request):
        response = super(QuickerExpirationAuthenticateView, self).get(request)
        request.session.set_expiry(settings.CLOUD_USER_SESSION_EXPIRATION)
        return response


class CloudUserClient(Client):
    authenticate_view = QuickerExpirationAuthenticateView
