#!/usr/bin/env bash

# This script executes "post-build" commands.

set -e

# Path to virtual environment (virtualenv) to which the specified
# project and its dependencies are installed.
VENV_PATH=$1; shift;

# Path to virtual environment (virtualenv) to which the specified
# project and its dependencies are installed.
INSTALL_PATH=$1; shift;

# Delete leftovers.
rm -rf $VENV_PATH
rm -rf $INSTALL_PATH
