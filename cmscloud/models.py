# -*- coding: utf-8 -*-
from cms.models.titlemodels import Title
from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
import requests


def trigger_restart():
    return
    #restarter = getattr(settings, 'RESTARTER_URL', None)
    #if not restarter:
    #    return
    #params = [('command', 'restart'), ('key', settings.SIMPLE_SSO_KEY)]
    #signature = build_signature(params, settings.SIMPLE_SSO_SECRET)
    #params.append(('signature', signature))
    #requests.post(restarter, dict(params))

def apphook_pre_checker(instance, **kwargs):
    """
    Store the old application_urls and path on the instance
    """
    try:
        instance._old_data = Title.objects.filter(pk=instance.pk).values_list('application_urls', 'path')[0]
    except IndexError:
        instance._old_data = (None, None)

def apphook_post_checker(instance, **kwargs):
    """
    Check if applciation_urls and path changed on the instance
    """
    old_apps, old_path = getattr(instance, '_old_data', (None, None))
    if old_apps != instance.application_urls:
        trigger_restart()
    elif old_path != instance.path and instance.application_urls:
        trigger_restart()

def apphook_post_delete_checker(instance, **kwargs):
    """
    Check if this was an apphook
    """
    if instance.application_urls:
        trigger_restart()

pre_save.connect(apphook_pre_checker, sender=Title)
post_save.connect(apphook_post_checker, sender=Title)
post_delete.connect(apphook_post_delete_checker, sender=Title)
