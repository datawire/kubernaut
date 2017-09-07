#!/bin/bash
set -e

# This is boilerplate that finds the directory the script lives in and
# puts it in the DIR variable.

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# REQUIRED CUSTOMIZATION:

# Set to the setuptools name for your project
PROJECT=kubernaut
# Set to the setuptools entrypoint for your binary
ENTRYPOINT=kubernaut.cli:cli
# Set to where you would like to save the pex binary
OUTPUT=out/kubernaut

# END REQUIRED_CUSTOMIZATION

# This assumes the script is in the project root. Change this if you
# move it into a subdirectory.
SRC_DIR=${DIR}

# The script will cache wheels here. Change this to whatever you want.
WHL_DIR=${DIR}/build/wheelhouse

# This will sync all various wheels (linux 32 bit, linux 64 bit, osx,
# etc) from S3 into a local directory so you can quickly build your
# cross platform python executable locally.
aws --no-sign-request s3 sync s3://datawire-wheelhouse/wheelhouse $WHL_DIR

cd "${WHL_DIR}"

# Temporary workaround until pex supports manylinux.
for whl in $(ls *-manylinux1_*.whl); do
  cp "${whl}" $(echo "${whl}" | sed s/manylinux1/linux/)
done

cd "${SRC_DIR}"

# This will package your python code up into a wheel.
pip wheel --no-index --no-deps . -w "${WHL_DIR}"

# This will use pex to assemble all the individual wheels (your
# project and all its dependencies) into a standalone cross platform
# executable.
pex --no-pypi \
    --disable-cache \
    -r requirements.txt "${PROJECT}" \
    -f "${WHL_DIR}" \
    -e "${ENTRYPOINT}" \
    -o "${OUTPUT}" \
    --platform linux_x86_64 \
    --platform linux_i686 \
    --platform macosx_10_11_x86_64

echo "Created ${OUTPUT}"