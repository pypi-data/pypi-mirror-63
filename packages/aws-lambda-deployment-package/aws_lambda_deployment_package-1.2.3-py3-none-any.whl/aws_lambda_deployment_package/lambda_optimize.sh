#!/usr/bin/env bash

function omit_venv() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/venv"
}

function omit_pip() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/pip"
    rm -rf "$PATH_TO_BUILD/pip-*"
}

function omit_setup() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/setuptools"
    rm -rf "$PATH_TO_BUILD/setuptools-*"
}

function omit_wheel() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/wheel"
    rm -rf "$PATH_TO_BUILD/wheel-*"
}

function omit_boto() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/boto"
    rm -rf "$PATH_TO_BUILD/boto3"
    rm -rf "$PATH_TO_BUILD/boto3-*"
    rm -rf "$PATH_TO_BUILD/botocore"
    rm -rf "$PATH_TO_BUILD/botocore-*"
    # Boto dependency.
    rm -rf "$PATH_TO_BUILD/s3transfer"
}

function omit_cfnlint() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/cfnlint"
}

function omit_moto() {
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/moto"
}

function omit_pycountry_locales() {
    # Lib pycountry has a bunch of localization that we don't use.
    PATH_TO_BUILD="$1"

    rm -rf "$PATH_TO_BUILD/pycountry/locales"
}