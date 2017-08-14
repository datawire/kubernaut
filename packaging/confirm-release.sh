#!/bin/bash
set -e

read -p "Continue with releasing version ${KUBERNAUT_VERSION} (y/n)? " choice
case "$choice" in
    y|Y ) echo "ok!";;
    n|N ) exit 1;;
    * ) exit 1;;
esac