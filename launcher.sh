#!/bin/bash
#echo "running smart_database in the background"
#python manage.py smart_database
echo "NOT running database migrations, because they should have already been run while building"
echo "running gunicorn"
python manage.py run_gunicorn -b 0.0.0.0:$PORT -w 2 --max-requests 1000 --graceful-timeout 120
echo "gunicorn stopped"