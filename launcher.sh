#!/bin/bash
if [ $PAGESPEED ]; then
  cp /etc/nginx/nginx-pagespeed.conf /etc/nginx/nginx.conf
else
  cp /etc/nginx/nginx-no-pagespeed.conf /etc/nginx/nginx.conf
fi
supervisord -c /etc/supervisor/supervisord.conf --nodaemon
