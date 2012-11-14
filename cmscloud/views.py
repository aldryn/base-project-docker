# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from cms.models.titlemodels import Title
from django.http import HttpResponse

def check_plugins(request):
    plugins = request.GET.get('plugins', '').split(',')
    count = CMSPlugin.objects.filter(plugin_type__in=plugins).count()
    return HttpResponse(str(count))

def check_apphooks(request):
    apphooks = request.GET.get('apphooks', '').split(',')
    count = Title.objects.filter(application_urls__in=apphooks).count()
    return HttpResponse(str(count))
