#!/bin/bash
echo "running smart_database in the background"
python manage.py smart_database &
DB_PID=$!
echo "running gunicorn"
python manage.py run_gunicorn -b 0.0.0.0:$PORT
wait $DB_PID