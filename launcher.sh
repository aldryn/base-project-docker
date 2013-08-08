#!/bin/bash
echo "running smart_database in the background"
python manage.py smart_database
echo "running gunicorn"
python manage.py run_gunicorn -b 0.0.0.0:$PORT
echo "gunicorn stopped"