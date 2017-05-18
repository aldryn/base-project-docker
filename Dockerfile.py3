FROM aldryn/base:py3-3.24
ADD stack /stack/base-project
ENV NPS_VERSION=1.11.33.2 \
    NGINX_VERSION=1.9.15 \
    NGINX_CONF_PATH=/etc/nginx/nginx.conf \
    NGINX_PROCFILE_PATH=/etc/nginx/nginx.procfile \
    NVM_DIR=/opt/nvm \
    NVM_VERSION=0.33.1

RUN /stack/base-project/install.sh

RUN mkdir -p /app && mkdir -p /data
WORKDIR /app
VOLUME /data

ENV PIP_PRE=1 \
    DATA_ROOT=/data
EXPOSE 80
CMD start web
