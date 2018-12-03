#!/bin/bash
set -x
set -e

PYTHON_MAJOR_VERSION=$(python -c 'import platform; print(platform.python_version_tuple()[0])')
PYTHON_SITE_PACKAGES_ROOT=$(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

${BASEDIR}/ngx_pagespeed.sh
${BASEDIR}/nvm.sh
cp ${BASEDIR}/add_addons_dev_to_syspath.py ${PYTHON_SITE_PACKAGES_ROOT}/add_addons_dev_to_syspath.py
cp ${BASEDIR}/add_addons_dev_to_syspath.pth ${PYTHON_SITE_PACKAGES_ROOT}/add_addons_dev_to_syspath.pth
