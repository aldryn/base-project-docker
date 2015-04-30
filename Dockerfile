FROM aldryn/base:2.4

RUN npm install -g crawl
WORKDIR /tmp
ENV NPS_VERSION 1.9.32.1
RUN wget https://github.com/pagespeed/ngx_pagespeed/archive/release-${NPS_VERSION}-beta.zip
RUN unzip release-${NPS_VERSION}-beta.zip
RUN cd ngx_pagespeed-release-${NPS_VERSION}-beta/ && \
    wget https://dl.google.com/dl/page-speed/psol/${NPS_VERSION}.tar.gz && \
    tar -xzvf ${NPS_VERSION}.tar.gz
ENV NGINX_VERSION 1.6.2
RUN wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
RUN tar -xvzf nginx-${NGINX_VERSION}.tar.gz
RUN cd nginx-${NGINX_VERSION} && \
    ./configure --prefix=/etc/nginx \
                --sbin-path=/usr/sbin/nginx \
                --conf-path=/etc/nginx/nginx.conf \
                --add-module=/tmp/ngx_pagespeed-release-${NPS_VERSION}-beta && \
    make && \
    make install
RUN rm -rf /tmp/*
ADD nginx /etc/nginx/
ADD supervisord.conf /etc/supervisor/supervisord.conf

WORKDIR /tmp
RUN wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz && \
    gunzip GeoIP.dat.gz && \
    mkdir /opt/geoip && \
    mv /tmp/GeoIP.dat /opt/geoip/ && \
    rm -rf /tmp/*

RUN mkdir -p /app
WORKDIR /app
ENV PIP_PRE 1

# support pip installing stuff from servers using TLS with SNI
RUN pip install pyOpenSSL==0.14 ndg-httpsclient==0.3.3 pyasn1==0.1.7 cryptography==0.7.2

ADD requirements.txt /app/
ADD generated_requirements.txt /app/
RUN pip install --use-wheel -r requirements.txt
ADD . /app/
EXPOSE 80
CMD start web
