from base_settings import *
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fobj:
    locals().update(json.load(fobj))

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
THUMBNAIL_QUALITY = 85
# THUMBNAIL_HIGH_RESOLUTION = False  # causing timeouts?
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
for app in ['filer', 'easy_thumbnails', 'mptt', 'polymorphic', 'cmsplugin_filer_file', 'cmsplugin_filer_image']:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
# end filer

# extra INSTALLED_APPS
for app in ['reversion']:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)


# extra MIDDLEWARE_CLASSES
for middleware in ['cmscloud.middleware.CurrentSiteMiddleware']:
    if not middleware in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES.append(middleware)