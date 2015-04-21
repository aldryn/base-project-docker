FROM aldryn/base:2.4

RUN npm install -g crawl
ADD build /build
RUN /build/prepare

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

# TODO: move to aldryn/base image
RUN curl -o /usr/local/bin/forego https://godist.herokuapp.com/projects/ddollar/forego/releases/current/linux-amd64/forego &&\
    chmod u+x /usr/local/bin/forego


ADD requirements.txt /app/
ADD generated_requirements.txt /app/
RUN pip install --use-wheel -r requirements.txt
ADD . /app/
ADD launch /launch
ENV GUNICORN_LOG_LEVEL info
ENV GUNICORN_WORKERS 2
ENV GUNICORN_TIMEOUT 120
ENV GUNICORN_MAX_REQUESTS 1000
ENV GUNICORN_PORT 80
EXPOSE 80
CMD start web
