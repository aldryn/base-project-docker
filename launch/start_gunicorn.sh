#!/bin/bash
if [ "$ENABLE_GEVENT" = true ]; then
    exec /app/launch/start_gunicorn_with_gevent.sh
else
    exec /app/launch/start_gunicorn_without_gevent.sh
fi
