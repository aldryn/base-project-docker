# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from cms.models.pagemodel import Page
from collections import defaultdict
from django.conf import settings
import json
from cmscloud.forms import AddForm, DeleteForm
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.generic import View
import os


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
