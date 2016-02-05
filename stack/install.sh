#!/bin/bash
set -x
set -e

PYTHON_MAJOR_VERSION=$(python -c 'import platform; print(platform.python_version_tuple()[0])')
PYTHON_SITE_PACKAGES_ROOT=$(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

${BASEDIR}/ngx_pagespeed.sh
${BASEDIR}/node.sh
${BASEDIR}/gulp.sh
${BASEDIR}/bower.sh
cp ${BASEDIR}/addons-dev.pth ${PYTHON_SITE_PACKAGES_ROOT}/aldryn-addons.pth
# TODO: check if this hack is needed in python3
cp ${BASEDIR}/fix_certifi_hack.py ${PYTHON_SITE_PACKAGES_ROOT}/fix_certifi_hack.py
cp ${BASEDIR}/fix_certifi_hack.pth ${PYTHON_SITE_PACKAGES_ROOT}/fix_certifi_hack.pth
