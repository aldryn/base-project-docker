FROM aldryn/base:2.1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install build-essential zlib1g-dev libpcre3 libpcre3-dev unzip wget supervisor npm
RUN ln -s /usr/bin/nodejs /usr/bin/node
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
RUN apt-get clean all
RUN rm -rf /tmp/*
ADD nginx /etc/nginx/
ADD supervisord.conf /etc/supervisor/supervisord.conf

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
ADD generated_requirements.txt /app/
RUN pip install --use-wheel -r requirements.txt
ADD . /app/
EXPOSE 80
CMD ["/app/launcher.sh"]
