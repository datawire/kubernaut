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

# this should have already been done... but it's not there either wtfsauce
gem install package_cloud

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

cat << EOF > app.json
{
  "application": "kubernaut",
  "latest_version": "${KUBERNAUT_VERSION}",
  "notices": []
}
EOF

printf "${KUBERNAUT_VERSION}" > out/stable.txt

export AWS_DEFAULT_REGION=us-east-1
aws s3api put-object \
    --bucket scout-datawire-io \
    --key kubernaut/app.json \
    --body app.json

aws s3api put-object \
    --bucket datawire-static-files \
    --key kubernaut/${KUBERNAUT_VERSION}/kubernaut \
    --body out/kubernaut

aws s3api put-object \
    --bucket datawire-static-files \
    --key kubernaut/stable.txt \
    --body out/stable.txt
