#!/bin/bash
python manage.py syncdb --noinput
python manage.py migrate
