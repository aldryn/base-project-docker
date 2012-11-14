#!/usr/bin/env python
from django.core.management import ManagementUtility
import os

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    utility = ManagementUtility(None)
    utility.execute()
