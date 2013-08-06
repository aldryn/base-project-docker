from base_settings import *
import os, json

fobj = open(os.path.join(os.path.dirname(__file__), 'settings.json'))
locals().update(json.load(fobj))
fobj.close()

CMS_LANGUAGES = {int(key) if isinstance(key, basestring) and key.isdigit() else key: value for key, value in CMS_LANGUAGES.items()}
