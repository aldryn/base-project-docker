from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
import re

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', {'insecure': True}),
    url(r'^admin/-djeese-api/', include('djeese_api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include('simple_sso.sso_client.urls')),
    url(r'^', include('cms.urls')),
)
