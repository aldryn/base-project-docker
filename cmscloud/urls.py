# -*- coding: utf-8 -*-
from cmscloud.views import Add, Delete
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    url(r'^check-plugins/$', 'cmscloud.views.check_plugins'),
    url(r'^check-apphooks/$', 'cmscloud.views.check_apphooks'),
    url(r'^add-file/$', csrf_exempt(Add.as_view())),
    url(r'^delete-file/$', csrf_exempt(Delete.as_view())),
)
