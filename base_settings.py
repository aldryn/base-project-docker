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

"""
{'HOME': '/home/vcap/app',
 'LANG': 'en_US.UTF-8',
 'LD_LIBRARY_PATH': '/app/.heroku/vendor/lib',
 'LIBRARY_PATH': '/app/.heroku/vendor/lib',
 'MEMORY_LIMIT': '64m',
 'OLDPWD': '/home/vcap',
 'PATH': '/home/vcap/app/.heroku/python/bin:/bin:/usr/bin',
 'PORT': '64467',
 'PWD': '/home/vcap/app',
 'PYTHONHASHSEED': 'random',
 'PYTHONHOME': '/app/.heroku/python',
 'PYTHONPATH': '/app/',
 'PYTHONUNBUFFERED': 'true',
 'SHLVL': '2',
 'TMPDIR': '/home/vcap/tmp',
 'USER': 'vcap',
 'VCAP_APPLICATION': '{"application_users":[],"instance_id":"a24db9877ac60859af39cb7376dc6b4c","instance_index":0,"application_version":"54f908d5-5b36-4c6f-8ad2-d699e7ebe502","application_name":"ojii-cftest-syncdb","application_uris":["ojii-cftest-syncdb.cfapps.io"],"started_at":"2013-06-21 07:47:00 +0000","started_at_timestamp":1371800820,"host":"0.0.0.0","port":64467,"limits":{"mem":64,"disk":1024,"fds":16384},"version":"54f908d5-5b36-4c6f-8ad2-d699e7ebe502","name":"ojii-cftest-syncdb","uris":["ojii-cftest-syncdb.cfapps.io"],"users":[],"start":"2013-06-21 07:47:00 +0000","state_timestamp":1371800820}',
 'VCAP_APP_HOST': '0.0.0.0',
 'VCAP_APP_PORT': '64467',
 'VCAP_CONSOLE_IP': '0.0.0.0',
 'VCAP_CONSOLE_PORT': '64468',
 'VCAP_SERVICES': {u'cleardb-n/a': [{u'credentials': {u'hostname': u'us-cdbr-east-04.cleardb.com',
                                    u'jdbcUrl': u'jdbc:mysql://bd7a8a30f87b67:4237fa6d@us-cdbr-east-04.cleardb.com:3306/ad_d60041824df843a',
                                    u'name': u'ad_d60041824df843a',
                                    u'password': u'4237fa6d',
                                    u'port': u'3306',
                                    u'uri': u'mysql://bd7a8a30f87b67:4237fa6d@us-cdbr-east-04.cleardb.com:3306/ad_d60041824df843a?reconnect=true',
                                    u'username': u'bd7a8a30f87b67'},
                   u'label': u'cleardb-n/a',
                   u'name': u'mysql-ojii-cftest',
                   u'plan': u'spark'}]},
 '_': '/home/vcap/app/.heroku/python/bin/python'}
"""

vcap_services = json.loads(os.environ['VCAP_SERVICES'])
mysql_srv = vcap_services['cleardb-n/a'][0]
cred = mysql_srv['credentials']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': cred['name'],
        'USER': cred['username'],
        'PASSWORD': cred['password'],
        'HOST': cred['hostname'],
        'PORT': cred['port'],
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
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'cms',
    'menus',
    'mptt',
    'south',
    'cms.plugins.text',
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
