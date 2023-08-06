#!/usr/bin/env bash

# This script executes "post-install" commands.

set -e

# Path under which a virtual environment folder should be created.
VENV_PATH=$1; shift;

SITE_PACKAGES_PATH=$VENV_PATH/lib/python3.6/site-packages/

# Source optimization functions.
THIS_SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
. "$THIS_SCRIPT_PATH/lambda_optimize.sh"

# Optimize according to flags.
while true; do
  case "$1" in
    --omit_boto ) omit_boto "$SITE_PACKAGES_PATH"; shift ;;
    --omit_wheels ) omit_wheel "$SITE_PACKAGES_PATH"; shift ;;
    --omit_pip ) omit_pip "$SITE_PACKAGES_PATH"; shift ;;
    --omit_setup ) omit_setup "$SITE_PACKAGES_PATH"; shift ;;
    --omit_cfnlint) omit_cfnlint "$SITE_PACKAGES_PATH"; shift ;;
    --omit_pycountry_locales) omit_pycountry_locales "$SITE_PACKAGES_PATH"; shift ;;
    --omit_moto) omit_moto "$SITE_PACKAGES_PATH"; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done
