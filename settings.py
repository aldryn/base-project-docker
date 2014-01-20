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
