#!/usr/bin/env bash

# This script creates a lambda build (zip package).

set -e

# Path to the installation directory whcih contains project
# source code and all installed dependencies.
INSTALL_PATH=$1; shift;

# A path where a build package (zip file) should be placed in.
BUILD_PATH=$1; shift;

# Create a zip and go back to an original dir.
CURRENT_DIR=$( pwd )
cd "$INSTALL_PATH"
shopt -s dotglob && zip -9 -r "$BUILD_PATH" *
cd "$CURRENT_DIR"
