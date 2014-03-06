from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from simple_sso.sso_client.client import Client

import re

admin.autodiscover()


client = Client.from_dsn(settings.SSO_DSN)


urlpatterns = patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', {'insecure': True}),
    url(r'^admin/~cmscloud-api/', include('cmscloud.urls')),
    url(r'^admin/~health-check/', include('health_check.urls')),
    url(r'^login/', include(client.get_urls())),
) + i18n_patterns('',
    # TODO: this should come from a "django-select2" addon... but how to include custom urls?
    url(r'^/api/~select2/', include('django_select2.urls')),  # required by: djangocms-link
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)
