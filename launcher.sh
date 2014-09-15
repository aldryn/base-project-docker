#!/bin/bash
gunicorn wsgi:application -b 0.0.0.0:$PORT  -w 2 --max-requests 1000 --graceful-timeout 120 --preload --worker-class gevent --config gunicorncfg.py --access-logfile - --error-logfile - --log-level info
