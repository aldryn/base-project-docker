# -*- coding: utf-8 -*-
from cms.cms_toolbar import CMSToolbar
from cms.toolbar.base import Toolbar
from cms.toolbar.constants import LEFT, RIGHT
from cms.toolbar.items import (Anchor, Switcher, TemplateHTML, ListItem, List, 
    GetButton)
from cms.utils import cms_static_url
from cms.utils.moderator import page_moderator_state, I_APPROVE
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import urllib


def _get_page_admin_url(context, toolbar, **kwargs):
    return reverse('admin:cms_page_change', args=(toolbar.request.current_page.pk,))

def _get_page_history_url(context, toolbar, **kwargs):
    return reverse('admin:cms_page_history', args=(toolbar.request.current_page.pk,))

def _get_add_child_url(context, toolbar, **kwargs):
    data = {
        'position': 'last-child',
        'target': toolbar.request.current_page.pk,
    }
    args = urllib.urlencode(data)
    return '%s?%s' % (reverse('admin:cms_page_add'), args)

def _get_add_sibling_url(context, toolbar, **kwargs):
    data = {
        'position': 'last-child',
    }
    if toolbar.request.current_page.parent_id:
        data['target'] = toolbar.request.current_page.parent_id
    args = urllib.urlencode(data)
    return '%s?%s' % (reverse('admin:cms_page_add'), args)

def _get_delete_url(context, toolbar, **kwargs):
    return reverse('admin:cms_page_delete', args=(toolbar.request.current_page.pk,))

def _get_approve_url(context, toolbar, **kwargs):
    return reverse('admin:cms_page_approve_page', args=(toolbar.request.current_page.pk,))

def _get_publish_url(context, toolbar, **kwargs):
    return reverse('admin:cms_page_publish_page', args=(toolbar.request.current_page.pk,))

class SSOCMSToolbar(CMSToolbar):
    def init(self):
        super(SSOCMSToolbar, self).init()

    def get_items(self, context, **kwargs):
        """
        Get the CMS items on the toolbar
        """
        items = [
            Anchor(LEFT, 'logo', _('django CMS'), 'https://www.django-cms.org'),
        ]
        
        self.page_states = []
        
        
        if self.is_staff:
            
            items.append(
                self.edit_mode_switcher
            )
            
            if self.request.current_page:
                states = self.request.current_page.last_page_states()
                has_states = states.exists()
                self.page_states = states
                if has_states:
                    items.append(
                        TemplateHTML(LEFT, 'status',
                                     'cms/toolbar/items/status.html')
                    )
                
                # publish button
                if self.edit_mode and settings.CMS_MODERATOR:
                    moderator_state = page_moderator_state(self.request, self.request.current_page)
                    should_approve = moderator_state['state'] >= I_APPROVE
                    has_perms = self.request.current_page.has_moderate_permission(self.request)
                    if should_approve and has_perms:
                        label = moderator_state['label']
                        urlgetter = _get_approve_url
                    elif has_perms:
                        label = _("Publish")
                        urlgetter = _get_publish_url
                    else:
                        urlgetter = _get_approve_url
                        label = _("Request Approval")
                    items.append(
                        GetButton(RIGHT, 'moderator', label, urlgetter)
                    )
            
                # The 'templates' Menu
                items.append(self.get_template_menu(context, self.can_change, self.is_staff))
                
                # The 'page' Menu
                items.append(self.get_page_menu(context, self.can_change, self.is_staff))
            
            # The 'Admin' Menu
            items.append(self.get_admin_menu(context, self.can_change, self.is_staff))
            
            items.append(
                GetButton(RIGHT, 'logout', _('Logout'), '?cms-toolbar-logout',
                          cms_static_url('images/toolbar/icons/icon_lock.png'))
            )
        elif not self.request.user.is_authenticated():
            items.append(
                GetButton(LEFT, 'logout', _('Login'), '%s?%s' % (reverse('simple-sso-login'), urllib.urlencode([('next', '%s?edit' % self.request.path)])))
            )
        else:
            items.append(
                GetButton(RIGHT, 'logout', _('Logout'), '?cms-toolbar-logout',
                          cms_static_url('images/toolbar/icons/icon_lock.png'))
            )
        return items
