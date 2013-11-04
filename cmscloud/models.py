# -*- coding: utf-8 -*-
from cms.models import Page
from django.core.signals import request_finished
from django.db.models.signals import post_save, pre_save, post_delete
from django.conf import settings
from cmscloud.template_api import registry
import requests

DISPATCH_UID = 'aldryn-cms-cloud-apphook'


def trigger_restart(**kwargs):
    request_finished.disconnect(trigger_restart, dispatch_uid=DISPATCH_UID)
    restarter_url = getattr(settings, 'RESTARTER_URL', None)
    if not restarter_url:
        return
    requests.post(restarter_url, data={
                  'info': getattr(settings, 'RESTARTER_PAYLOAD', None)})


def apphook_pre_checker(instance, **kwargs):
    """
    Store the old application_urls and path on the instance
    """
    try:
        page = Page.objects.get(pk=instance.pk)
    except Page.DoesNotExist:
        instance._old_data = (None, None)
        return
    paths = sorted(page.title_set.values_list('path', flat=True))
    instance._old_data = (page.application_urls, paths)


def apphook_post_checker(instance, **kwargs):
    """
    Check if applciation_urls and path changed on the instance
    """
    old_apps, old_paths = getattr(instance, '_old_data', (None, None))
    if old_apps != instance.application_urls:
        request_finished.connect(trigger_restart, dispatch_uid=DISPATCH_UID)
    else:
        paths = sorted(instance.title_set.values_list('path', flat=True))
        if old_paths != paths and instance.application_urls:
            request_finished.connect(
                trigger_restart, dispatch_uid=DISPATCH_UID)


def apphook_post_delete_checker(instance, **kwargs):
    """
    Check if this was an apphook
    """
    if instance.application_urls:
        request_finished.connect(trigger_restart, dispatch_uid=DISPATCH_UID)

pre_save.connect(apphook_pre_checker, sender=Page)
post_save.connect(apphook_post_checker, sender=Page)
post_delete.connect(apphook_post_delete_checker, sender=Page)


def live_reload():
    live_reload_credential_url = getattr(
        settings, 'LIVERELOAD_CREDENTIAL_URL', None)
    if not live_reload_credential_url:
        return ''
    return '''<script src="https://static.django-cms.com/javascripts/libs/klass.js" type="text/javascript"></script>
    <script src="https://static.django-cms.com/javascripts/libs/autobahn.min.js" type="text/javascript"></script>
    <script src="https://static.django-cms.com/javascripts/realtime.js" type="text/javascript"></script>
    <script src="https://static.django-cms.com/javascripts/livereload.js" type="text/javascript"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            LiveReload({
                "credential_url": "%s",
                "logged_user_email": "{{ request.user.email }}",
            });
        });
    </script>''' % live_reload_credential_url

registry.add_to_tail(live_reload())
