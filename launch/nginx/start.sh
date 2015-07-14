#!/bin/bash
SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")
export GUNICORN_PORT=5000
cp ${BASEDIR}/nginx.conf /etc/nginx/nginx.conf
/bin/sed -i "s/DOMAIN/${DOMAIN}/" /etc/nginx/nginx.conf
exec forego start -f ${BASEDIR}/Procfile
