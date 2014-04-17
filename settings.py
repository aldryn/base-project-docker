# -*- coding: utf-8 -*-
import json
import os

from base_settings import *  # NOQA

with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fobj:
    locals().update(json.load(fobj))

# all strings are unicode after loading from json. But some settings MUST BE STRINGS
if isinstance(locals().get('EMAIL_HOST_PASSWORD', None), unicode):
    EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD.encode('ascii')


CMS_LANGUAGES = {int(key) if isinstance(key, basestring) and key.isdigit() else key: value for key, value in CMS_LANGUAGES.items()}

with open(os.path.join(os.path.dirname(__file__), 'cms_templates.json')) as fobj:
    locals()['CMS_TEMPLATES'] = json.load(fobj)


if 'DATABASES' not in locals():
    localname = os.environ.get("LOCAL_DATABASE_NAME", ":memory:")
    print "USING IN %s SQLITE3" % localname
    print "NO DATABASE CONFIGURED!!! USING %s SQLITE3 DATABASE!!!"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': localname,
        }
    }

# TODO: remove django-filer stuff from here. It should be an addon.
THUMBNAIL_QUALITY = 90
# THUMBNAIL_HIGH_RESOLUTION = False  # FIXME: enabling THUMBNAIL_HIGH_RESOLUTION causes timeouts/500!
THUMBNAIL_PRESERVE_EXTENSIONS = ['png', 'gif']
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_SOURCE_GENERATORS = (
    'easy_thumbnails.source_generators.pil_image',
)
FILER_IMAGE_USE_ICON = True
for app in ['filer', 'easy_thumbnails', 'mptt', 'polymorphic', 'cmsplugin_filer_file', 'cmsplugin_filer_image']:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
# end filer

# extra INSTALLED_APPS
extra_installed_apps = [
    'reversion',
    # TODO: remove all plugins from here. they should be addons
    'djangocms_text_ckeditor',
    # 'cms.plugins.picture',  # now using django-filer
    'djangocms_link',  # 'cms.plugins.link',
    'django_select2',  # required by djangocms-link
    # 'cms.plugins.file',  # now using django-filer
    'djangocms_snippet',  # 'cms.plugins.snippet',
    'djangocms_googlemap',  # 'cms.plugins.googlemap',
]
for app in extra_installed_apps:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)


# extra MIDDLEWARE_CLASSES
EXTRA_MIDDLEWARE_CLASSES = [
    'cmscloud.middleware.CurrentSiteMiddleware',
    'cmscloud.middleware.AldrynUserMiddleware']
for middleware in EXTRA_MIDDLEWARE_CLASSES:
    if not middleware in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES.append(middleware)


# TODO: move this to ckeditor addon aldyn config when we extract it from the base project
# boilerplate should provide /static/js/modules/ckeditor.wysiwyg.js and /static/css/base.css
CKEDITOR_SETTINGS = {
    'height': 300,
    'stylesSet': 'default:/static/js/modules/ckeditor.wysiwyg.js',
    'contentsCss': ['/static/css/base.css'],
    'language': '{{ language }}',
    'toolbar': 'CMS',
    'skin': 'moono',
    'extraPlugins': 'cmsplugins',
}


# OPTIONAL REDIS
REDIS_URL = locals().get('REDIS_URL', '')
if REDIS_URL:
    import dj_redis_url
    redis = dj_redis_url.parse(REDIS_URL)
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': str(redis['HOST']) + ':' + str(redis['PORT']),  # '{HOST}:{PORT}'.format(redis),
            'OPTIONS': {
                'DB': 10,
                'PASSWORD': redis['PASSWORD'],
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 50,
                    'timeout': 20,
                },
                'MAX_CONNECTIONS': 1000,
            },
        },
    }


# django-health-check
for app in [
        'health_check',
        'health_check_db',
        'health_check_cache',
        # 'health_check_storage',
]:
    INSTALLED_APPS.append(app)

if 'CMSCLOUD_SYNC_KEY' not in locals():
    CMSCLOUD_SYNC_KEY = None
if 'LAST_BOILERPLATE_COMMIT' not in locals():
    LAST_BOILERPLATE_COMMIT = None
if 'SYNC_CHANGED_FILES_URL' not in locals():
    SYNC_CHANGED_FILES_URL = None
