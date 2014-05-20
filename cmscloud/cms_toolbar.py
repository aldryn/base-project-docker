# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from django.conf import settings
from django.core.urlresolvers import reverse

from cmscloud.views import LIVERELOAD_ACTIVE_SESSION_KEY, LIVERELOAD_ACTIVE_DEFAULT


@toolbar_pool.register
class LiveReloadToggleButton(CMSToolbar):
    def populate(self):
        if hasattr(settings, 'LIVERELOAD_CREDENTIAL_URL'):
            url = reverse('toggle-livereload')
            active = self.request.session.get(LIVERELOAD_ACTIVE_SESSION_KEY, LIVERELOAD_ACTIVE_DEFAULT)
            self.toolbar.add_button('Live Reload', url, active=active, side=self.toolbar.RIGHT)
