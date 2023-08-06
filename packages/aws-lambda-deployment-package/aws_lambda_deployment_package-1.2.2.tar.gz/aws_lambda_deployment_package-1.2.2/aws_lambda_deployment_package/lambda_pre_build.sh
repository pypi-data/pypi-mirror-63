#!/usr/bin/env bash

# This script executes "pre-build" commands.

set -e

# Path to virtual environment (virtualenv) to which the specified
# project and its dependencies are installed.
VENV_PATH=$1; shift;

# Path to virtual environment (virtualenv) to which the specified
# project and its dependencies are installed.
INSTALL_PATH=$1; shift;

# Path to virtual environment (virtualenv) to which the specified
# project and its dependencies are installed.
PROJECT_PATH=$1; shift;

mkdir $INSTALL_PATH

# Copy all material into a separate install folder.
cp -R $PROJECT_PATH/. $INSTALL_PATH
cp -R $VENV_PATH/lib/python3.6/site-packages/. $INSTALL_PATH
