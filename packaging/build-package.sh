#!/bin/bash
# This will be run inside a Docker image for each operating system, which is
# presumed to have fpm pre-installed.
#
# Inputs:
# $PACKAGE_VERSION is the package version to use.
# $PACKAGE_TYPE is rpm or deb.
# Command line arguments are the dependencies.
set -e

# Set proper ownership before exiting, so the created packages aren't owned by
# root.
trap 'chown -R --reference /build-inside/build-package.sh /out/' EXIT

# Package only includes /usr/bin/telepresence:
mkdir /tmp/build
cp /source/kubernaut /tmp/build
cd /out
fpm -t "$PACKAGE_TYPE" \
    --name kubernaut \
    --version "$PACKAGE_VERSION" \
    --description "Command-line client for Kubernaut.io" \
    ${@/#/--depends } \
    --prefix /usr/bin \
    --chdir /tmp/build \
    --input-type dir \
    kubernaut
