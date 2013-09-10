# -*- coding: utf-8 -*-
from django.conf import settings

def google_analytics(request):
    return {'GOOGLE_ANALYTICS_KEY': getattr(settings, 'GOOGLE_ANALYTICS_KEY', None)}

def boilerplate(request):
    return {'BOILERPLATE_CONFIG': getattr(settings, 'BOILERPLATE_CONFIG', {})}
