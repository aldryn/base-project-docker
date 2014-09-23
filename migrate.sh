#!/bin/bash
set -x  # echo on
# createcachetable must NOT be last,
# because it will return an error code if the table already exists and that would make the whole script fail
python manage.py createcachetable django_dbcache
python manage.py syncdb --noinput
python manage.py migrate
