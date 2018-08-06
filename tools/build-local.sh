#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

pyinstaller kubernaut/cli.py \
    --distpath "build/out" \
    --name ${BINARY_NAME} \
    --onefile \
    --workpath build
