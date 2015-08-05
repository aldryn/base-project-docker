FROM minimal_base

ADD build /build
ENV NPS_VERSION=1.9.32.3\
    NGINX_VERSION=1.6.3
RUN /build/prepare

RUN mkdir -p /app
WORKDIR /app
ENV PIP_PRE 1

# support pip installing stuff from servers using TLS with SNI
#RUN pip install pyOpenSSL==0.15.1 ndg-httpsclient==0.3.3 pyasn1==0.1.7 cryptography==0.8.2
ENV GUNICORN_LOG_LEVEL=info\
    GUNICORN_WORKERS=2\
    GUNICORN_TIMEOUT=120\
    GUNICORN_MAX_REQUESTS=1000\
    GUNICORN_PORT=80\
    ENABLE_GEVENT=false\
    PATH=/app/node_modules/.bin:$PATH
EXPOSE 80
CMD start web

ONBUILD ADD . /app
ONBUILD RUN if [ -f requirements.in ] ; then pip-compile requirements.in; fi
ONBUILD RUN if [ -f requirements.txt ] ; then pip install --trusted-host mypypi.local.aldryn.net --find-links=https://mypypi.local.aldryn.net -r requirements.txt; fi
ONBUILD RUN if [ -f package.json ] ; then npm install; fi
