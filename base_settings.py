# -*- coding: utf-8 -*-
import os
import json

gettext = lambda s: s

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_ROOT = os.path.join(PROJECT_DIR, 'data')

TEMPLATE_DEBUG = DEBUG = False

MANAGERS = ADMINS = ()

LANGUAGES = [('en', 'en')]
DEFAULT_LANGUAGE = 0

try:
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    psql_srv = vcap_services['postgresql-9.1'][0]
    cred = psql_srv['credentials']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': cred['name'],
            'USER': cred['username'],
            'PASSWORD': cred['password'],
            'HOST': cred['hostname'],
            'PORT': cred['port'],
        }
    }
except:
    import traceback; traceback.print_exc()
    print os.environ
    print "FAILED TO GET DATABASE CREDENTIALS!!!"
    localname = os.environ.get("LOCAL_DATABASE_NAME", ":memory:")
    print "USING IN %s SQLITE3" % localname
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': localname,
        }
    }

TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_L10N = USE_I18N = True


MEDIA_ROOT = os.path.join(DATA_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(DATA_ROOT, 'static')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'custom_static'),
    os.path.join(PROJECT_DIR, 'static'),
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'cms.context_processors.media',
    'cmscloud.context_processors.google_analytics',
    'cmscloud.context_processors.boilerplate',
    'cmscloud.template_api.template_processor',
]

CMS_TEMPLATES = [
    ('main.html', 'Full width'),
    ('main_sidebar.html', 'Sidebar right'),
    ('sidebar_main.html', 'Sidebar left'),
]

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'custom_templates'),
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'djangocms_admin_style',  # must be before admin to override base template
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'cms',
    'cms.stacks',
    'menus',
    'mptt',
    'south',
    'djangocms_text_ckeditor',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'raven.contrib.django',
    'sekizai',
    'gunicorn',
    'cmscloud',
]
