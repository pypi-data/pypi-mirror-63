#!/usr/bin/env bash

# This script installs a given project to a given virtual environment.

set -e

# The environment of the python project.
# Environment can be one of the following: none, dev, prod.
# If environment is specified as dev or prod, an "install-option"
# parameter is supplied to "pip install" command.
ENVIRONMENT=$1; shift;

# Path to the project's source code to build (e.g. /path/to/my/project).
# When building a deployment package, all files under given path will be included
# in the deployment package.
PROJECT_SOURCE_PATH=$1; shift;

# Path to virtual environment (virtualenv) to which the specified
# project and its dependencies should be installed. This script enforces
# you to use virtual environments as it is an extremely best practice to
# keep global python interpreters clean.
VENV_PATH=$1; shift;

# Source virtual env.
. "$VENV_PATH"/bin/activate

# Save the original path so later we can come back to the original place.
# This is necessary to keep consistency in the scripts and current path
# under control.
TEMP_CURRENT_PATH=$( pwd )

# Go to the provided project path and do all actions in that directory.
cd $PROJECT_SOURCE_PATH

# Remove leftovers.
rm -rf *.egg-info build dist

# Create project's source distribution.
# Read more about this command here:
# https://docs.python.org/3.6/distutils/sourcedist.html
python setup.py sdist

if [[ "$ENVIRONMENT" = "none" ]]; then
    # Install the package.
    # Read more about installing python packages here:
    # https://packaging.python.org/tutorials/installing-packages/
    python -m pip install dist/*
elif [[ "$ENVIRONMENT" = "dev" || "$ENVIRONMENT" = "prod" ]]
then
    # Install the package by passing custom options with "install-option".
    # Read more about this:
    # https://pip.pypa.io/en/stable/reference/pip_install/#id30
    python -m pip install dist/* --install-option=--environment=$ENVIRONMENT
else
    echo "Unsupported environment - should be prod or dev."
    # Remove leftovers.
    rm -rf *.egg-info build dist
    exit 1
fi

# Remove leftovers.
rm -rf *.egg-info build dist
# Get back to the original path.
cd $TEMP_CURRENT_PATH
