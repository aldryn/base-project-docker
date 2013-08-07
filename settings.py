from base_settings import *
import os, json

fobj = open(os.path.join(os.path.dirname(__file__), 'settings.json'))
locals().update(json.load(fobj))
fobj.close()

CMS_LANGUAGES = {int(key) if isinstance(key, basestring) and key.isdigit() else key: value for key, value in CMS_LANGUAGES.items()}


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