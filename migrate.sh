#!/bin/bash
set -x  # echo on
# createcachetable must NOT be last,
# because it will return an error code if the table already exists and that would make the whole script fail
python manage.py createcachetable django_dbcache
set -e
python manage.py syncdb --noinput
python manage.py migrate --list --noinput
python manage.py migrate --noinput
python manage.py migrate --list --noinput
# unfortunatly deleting orphaned plugins fails for plugins of Addons that are no longer installed.
# and that can happen quickly if you uninstall an Addon. We need to implement a cleaner uninstall
# first.
#echo "cms: deleting orphaned plugins"
#python manage.py cms delete_orphaned_plugins --noinput
echo "cms: fixing mptt-tree"
python manage.py cms fix-mptt --noinput

