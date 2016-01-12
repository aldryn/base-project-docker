FROM aldryn/base:3.1
ADD build /build
ENV NPS_VERSION=1.9.32.3\
    NGINX_VERSION=1.6.3\
    NGINX_CONF_PATH=/etc/nginx/nginx.conf\
    NGINX_PROCFILE_PATH=/etc/nginx/nginx.procfile\
    NODE_VERSION=4.2.4\
    NPM_VERSION=2.14.12
RUN /build/prepare

RUN mkdir -p /app && mkdir -p /data
WORKDIR /app
VOLUME /data

ENV PIP_PRE=1\
    DATA_ROOT=/data
EXPOSE 80
CMD start web
