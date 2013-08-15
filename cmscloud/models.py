# -*- coding: utf-8 -*-
from cms.models import Page
from django.core.signals import request_finished
from django.db.models.signals import post_save, pre_save, post_delete
from django.conf import settings
import requests


def trigger_restart(**kwargs):
    restarter_url = getattr(settings, 'RESTARTER_URL', None)
    if not restarter_url:
        return
    requests.post(restarter_url, data={'info': getattr(settings, 'RESTARTER_PAYLOAD', None)})

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
        request_finished.connect(trigger_restart, dispatch_uid='aldryn-cms-cloud-apphook')
    else:
        paths = sorted(instance.title_set.values_list('path', flat=True))
        if old_paths != paths and instance.application_urls:
            request_finished.connect(trigger_restart, dispatch_uid='aldryn-cms-cloud-apphook')

def apphook_post_delete_checker(instance, **kwargs):
    """
    Check if this was an apphook
    """
    if instance.application_urls:
        request_finished.connect(trigger_restart, dispatch_uid='aldryn-cms-cloud-apphook')

pre_save.connect(apphook_pre_checker, sender=Page)
post_save.connect(apphook_post_checker, sender=Page)
post_delete.connect(apphook_post_delete_checker, sender=Page)
