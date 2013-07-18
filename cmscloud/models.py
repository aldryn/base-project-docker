# -*- coding: utf-8 -*-
from cms.models import Page
from django.db.models.signals import post_save, pre_save, post_delete


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
        trigger_restart()
    else:
        paths = sorted(instance.title_set.values_list('path', flat=True))
        if old_paths != paths and instance.application_urls:
            trigger_restart()

def apphook_post_delete_checker(instance, **kwargs):
    """
    Check if this was an apphook
    """
    if instance.application_urls:
        trigger_restart()

pre_save.connect(apphook_pre_checker, sender=Page)
post_save.connect(apphook_post_checker, sender=Page)
post_delete.connect(apphook_post_delete_checker, sender=Page)
