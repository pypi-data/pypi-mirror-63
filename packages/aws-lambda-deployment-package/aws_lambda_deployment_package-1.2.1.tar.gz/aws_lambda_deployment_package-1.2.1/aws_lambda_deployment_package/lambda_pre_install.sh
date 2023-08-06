#!/usr/bin/env bash

# This script executes pre-install commands.

set -e

# Path under which a virtual environment folder should be created.
VENV_PATH=$1; shift;

# Create new virtual env.
virtualenv $VENV_PATH --python=python3.6

# Source virtual env.
. $VENV_PATH/bin/activate

# Ensure pip version 18.1.
python -m pip install pip==18.1
