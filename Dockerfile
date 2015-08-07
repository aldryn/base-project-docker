FROM minimal_base

ADD build /build
ENV NPS_VERSION=1.9.32.3\
    NGINX_VERSION=1.6.3\
    NGINX_CONF_PATH=/etc/nginx/nginx.conf
RUN /build/prepare

RUN mkdir -p /app && mkdir -p /data
WORKDIR /app
VOLUME /data

# support pip installing stuff from servers using TLS with SNI
#RUN pip install pyOpenSSL==0.15.1 ndg-httpsclient==0.3.3 pyasn1==0.1.7 cryptography==0.8.2
ENV PATH=/app/node_modules/.bin:$PATH\
    PIP_PRE=1\
    DATA_ROOT=/data
EXPOSE 80
CMD start web
