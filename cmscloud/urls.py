# -*- coding: utf-8 -*-
from cmscloud.views import Add, Delete, get_currently_logged_in_user_email
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    url(r'^check-uninstall/$', 'cmscloud.views.check_uninstall_ok'),
    url(r'^add-file/$', csrf_exempt(Add.as_view())),
    url(r'^delete-file/$', csrf_exempt(Delete.as_view())),
    url(r'^currently-logged-in-user-email/$', get_currently_logged_in_user_email,
        name='currently-logged-in-user-email'),
)
