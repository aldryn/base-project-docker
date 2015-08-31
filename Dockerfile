FROM aldryn/base:3.0

# START
# duplicate of Dockerfile here, until we figure out some sort of chained
# building and dynamic FROM for the build and onbuild versions.
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

# support pip installing stuff from servers using TLS with SNI
#RUN pip install pyOpenSSL==0.15.1 ndg-httpsclient==0.3.3 pyasn1==0.1.7 cryptography==0.8.2
ENV PATH=/app/node_modules/.bin:$PATH\
    PIP_PRE=1\
    DATA_ROOT=/data
EXPOSE 80
CMD start web
# END

# TODO: be smarter here to prevent re-building on every little source change
#       possible workaround to not being able to add a specific file only if it
#       exists: add a directory somewhere else in the filesystem and then move
#       and execute it if it exists.
ONBUILD ADD . /app
ONBUILD RUN if [[ -f requirements.in ]] ; then pip-compile --verbose requirements.in; fi
ONBUILD RUN if [[ -f requirements.txt ]] ; then pip install --no-cache-dir -r requirements.txt; fi
ONBUILD RUN if [[ -f package.json ]] ; then npm install --verbose; fi
ONBUILD RUN if [[ -f bower.json && -f .bowerrc ]] ; then bower install --verbose; fi
ONBUILD RUN DJANGO_MODE=build python manage.py collectstatic --noinput --link
