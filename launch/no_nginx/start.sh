#!/bin/bash
SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")
exec forego start -f ${BASEDIR}/Procfile
