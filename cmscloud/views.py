# -*- coding: utf-8 -*-
from collections import defaultdict
import inspect
import json
import os

from cms.app_base import CMSApp
from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.utils.django_load import get_module
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.generic import View

from cmscloud.forms import AddForm, DeleteForm


def check_uninstall_ok(request):
    apps = request.GET.get('apps', '').split(',')
    if apps == ['']:
        return HttpResponseBadRequest("no apps provided")
    plugin_names = []
    apphooks = []
    menus = []
    for app in apps:
        module = get_module(app, "cms_plugins", False, False)
        if module:
            for cls_name in dir(module):
                print cls_name
                cls = getattr(module, cls_name)
                if inspect.isclass(cls) and issubclass(cls, CMSPluginBase):
                    plugin_names.append(cls.__name__)
        module = get_module(app, "cms_app", False, False)
        if module:
            for cls_name in dir(module):
                cls = getattr(module, cls_name)
                if inspect.isclass(cls) and issubclass(cls, CMSApp) and not cls.__name__ in apphooks:
                    apphooks.append(cls.__name__)
        module = get_module(app, "menu", False, False)
        if module:
            for cls_name in dir(module):
                cls = getattr(module, cls_name)
                if hasattr(cls, 'cms_enabled') and cls.cms_enabled and not cls.__name__ in menus:
                    menus.append(cls.__name__)
    plugin_count = {}
    for plugin_type in plugin_names:
        count = CMSPlugin.objects.filter(plugin_type=plugin_type).count()
        if count:
            plugin_count[plugin_type] = count
    apphook_count = []
    for hook in apphooks:
        exists = Page.objects.filter(application_urls=hook).exists()
        if exists:
            apphook_count.append(hook)
    menu_count = []
    for menu in menus:
        exists = Page.objects.filter(navigation_extenders=menu).exists()
        if exists:
            menu_count.append(menu)
    if plugin_count or apphook_count or menu_count:
        result = {'plugins': plugin_count, 'apphooks': apphook_count, 'menus': menu_count}
    else:
        result = 'ok'
    return HttpResponse(json.dumps(result), content_type="application/json")


def check_plugins(request):
    plugins = request.GET.get('plugins', '').split(',')
    count = CMSPlugin.objects.filter(plugin_type__in=plugins).count()
    return HttpResponse(str(count))


def check_apphooks(request):
    apphooks = request.GET.get('apphooks', '').split(',')
    count = Page.objects.filter(application_urls__in=apphooks).count()
    return HttpResponse(str(count))


def errors_to_json(form):
    output = defaultdict(list)
    for field, errors in form.errors.items():
        for error in errors:
            output[form[field].label if field != NON_FIELD_ERRORS else NON_FIELD_ERRORS].append(error)
    return json.dumps(output)


class Add(View):
    form = AddForm

    def post(self, request):
        if not getattr(settings, 'CMSCLOUD_SYNC_KEY'):
            raise Http404()
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            self.save(form.clean())
            return HttpResponse('', status=204)
        else:
            return HttpResponseBadRequest(errors_to_json(form), content_type='application/json')

    def save(self, data):
        full_path = os.path.join(settings.PROJECT_DIR, data['path'])
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(full_path, 'w') as fobj:
            for chunk in data['content'].chunks():
                fobj.write(chunk)


class Delete(Add):
    form = DeleteForm

    def save(self, data):
        full_path = os.path.join(settings.PROJECT_DIR, data['path'])
        if os.path.exists(full_path):
            os.remove(full_path)


@login_required
def get_currently_logged_in_user_email(request):
    return HttpResponse(request.user.email, content_type='text/plain')
