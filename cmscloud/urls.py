# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^check-plugins/$', 'cmscloud.views.check_plugins'),
    url(r'^check-apphooks/$', 'cmscloud.views.check_apphooks'),
)
