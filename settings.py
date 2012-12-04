from base_settings import *
import os, json

fobj = open(os.path.join(os.path.dirname(__file__), 'settings.json'))
locals().update(json.load(fobj))
fobj.close()
