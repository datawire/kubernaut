#!/bin/bash
set -e

# Clone blackbird-homebrew:
BUILD_HOMEBREW_DIR=$(mktemp --directory)
echo "Cloning into ${BUILD_HOMEBREW_DIR}..."
git clone git@github.com:datawire/homebrew-blackbird.git "${BUILD_HOMEBREW_DIR}"
FORMULA="${BUILD_HOMEBREW_DIR}/Formula/kubernaut.rb"

# Update recipe
cp packaging/homebrew-formula.rb "$FORMULA"
sed "s/__NEW_VERSION__/${KUBERNAUT_VERSION}/g" -i "$FORMULA"
TARBALL_HASH=$(curl --silent -L "https://gitlab.com/datawire/kubernaut/repository/archive.tar.gz?ref=${KUBERNAUT_VERSION}" | sha256sum | cut -f 1 -d " ")
sed "s/__TARBALL_HASH__/${TARBALL_HASH}/g" -i "$FORMULA"
cd "${BUILD_HOMEBREW_DIR}"
git add "$FORMULA"
git commit -m "Release ${KUBERNAUT_VERSION}"
git push origin master
