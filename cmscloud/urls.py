# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^check-plugins/$', 'djeese_api.views.check_plugins'),
    url(r'^check-apphooks/$', 'djeese_api.views.check_apphooks'),
)
