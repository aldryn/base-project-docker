#!/bin/bash
BASEDIR=/launch/nginx_pagespeed_and_browsercache
cp ${BASEDIR}/nginx.conf /etc/nginx/nginx.conf
/bin/sed -i "s/DOMAIN/${DOMAIN}/" /etc/nginx/nginx.conf
exec forego start -f ${BASEDIR}/Procfile -e ${BASEDIR}/.env
