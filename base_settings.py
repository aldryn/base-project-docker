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

TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_L10N = USE_I18N = True


MEDIA_ROOT = os.path.join(DATA_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(DATA_ROOT, 'static_collected')
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# WARN: these are all overwritten from settings.json! (I think)
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'cms.context_processors.media',
    'cmscloud.context_processors.boilerplate',
    'cmscloud.context_processors.debug',
    'aldryn_snake.template_api.template_processor',
]

CMS_TEMPLATES = [
    ('main.html', 'Full width'),
    ('main_sidebar.html', 'Sidebar right'),
    ('sidebar_main.html', 'Sidebar left'),
]

ROOT_URLCONF = 'urls'

CMSCLOUD_STATIC_URL = 'https://static.aldryn.com/'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIR, 'cmscloud/templates'),
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'custom_templates'),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

###############################################################################
# Cloud user authentication
###############################################################################

# User can change its data on Login's server.
# We cannot do a sync of "recently changed" user data due to these reasons:
# - security risk, leaking user data to unauthorized websites,
# - it would require some periodic tasks (celery?),
# - stage websites are being paused during which the sync wouldn't work
CLOUD_USER_SESSION_EXPIRATION = 24 * 60 * 60  # 24h = 1day
