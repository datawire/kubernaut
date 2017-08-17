#!/bin/bash
# Run the release!
set -e

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    exit 0;
fi

# Store the SSH key used to push to github.com/datawire/homebrew-blackbird; this
# key is set as environment variable on Travis repo:
openssl aes-256-cbc -K $encrypted_a76edca1e45a_key -iv $encrypted_a76edca1e45a_iv -in packaging/homebrew_rsa.enc -out packaging/homebrew_rsa -d
chmod 600 packaging/homebrew_rsa

# Add ssh keys we need to push to github.com/datawire/homebrew-blackbird:
eval $(ssh-agent)
ssh-add packaging/homebrew_rsa

# Run the release:
make release

cat << EOF > ~/.pypirc
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
username=d6e-automaton
password=${PYPI_PASSWORD}

[pypitest]
username=d6e-automaton
password=${PYPI_PASSWORD}
EOF

python setup.py sdist upload -r pypi
