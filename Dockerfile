FROM aldryn/base:3.0
ADD build /build
ENV NPS_VERSION=1.9.32.3\
    NGINX_VERSION=1.6.3\
    NGINX_CONF_PATH=/etc/nginx/nginx.conf\
    NGINX_PROCFILE_PATH=/etc/nginx/nginx.procfile\
    NODE_VERSION=0.10.40\
    NPM_VERSION=2.13.3
RUN /build/prepare

RUN mkdir -p /app && mkdir -p /data
WORKDIR /app
VOLUME /data

ENV PATH=/app/node_modules/.bin:$PATH\
    PIP_PRE=1\
    DATA_ROOT=/data
EXPOSE 80
CMD start web
