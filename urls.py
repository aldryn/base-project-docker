from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from simple_sso.sso_client.client import Client

import re

admin.autodiscover()


client = Client.from_dsn(settings.SSO_DSN)


urlpatterns = patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', {'insecure': True}),
    url(r'^admin/-djeese-api/', include('cmscloud.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include(client.get_urls())),
    url(r'^', include('cms.urls')),
)
