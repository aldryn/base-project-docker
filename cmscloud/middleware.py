# -*- coding: utf-8 -*-
"""
Edit Toolbar middleware
"""
from cmscloud.cms_toolbar import SSOCMSToolbar
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from simple_sso.sso_client.client import LoginView, Client


def toolbar_plugin_processor(instance, placeholder, rendered_content, original_context):
    original_context.push()
    data = {
        'instance': instance,
        'rendered_content': rendered_content
    }
    original_context.update(data)
    output = render_to_string('cms/toolbar/placeholder_wrapper.html', original_context)
    original_context.pop()
    return output

class ToolbarMiddleware(object):
    """
    Middleware to set up CMS Toolbar.
    """

    def process_request(self, request):
        """
        If we should show the toolbar for this request, put it on
        request.toolbar. Then call the request_hook on the toolbar.
        """
        if 'edit' in request.GET and not request.session.get('cms_edit', False):
            request.session['cms_edit'] = True
        request.toolbar = SSOCMSToolbar(request)

    def process_view(self, request, view_func, view_args, view_kwarg):
        response = request.toolbar.request_hook()
        if isinstance(response, HttpResponse):
            return response


class AccessControlMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated() and not request.path.startswith('/login/'):
            view = LoginView.as_view(client=Client.from_dsn(settings.SSO_DSN))
            return view(request)
        return None
