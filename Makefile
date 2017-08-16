.PHONY: default release

VERSION=$(shell git describe --tags)
SHELL:=/bin/bash

default:
	@echo "See https://github.com/datawire/kubernaut/README.md"

version:
	@echo $(VERSION)

build: virtualenv
	tox -e py3

## Setup dependencies ##

virtualenv:
	virtualenv --python=python3 virtualenv
	virtualenv/bin/pip install -Ur dev-requirements.txt

## Development ##

## Release ##

# Will be run in Travis CI on tagged commits
release: virtualenv build
#	env KUBERNAUT_VERSION=$(VERSION) packaging/homebrew-package.sh
	env KUBERNAUT_VERSION=$(VERSION) packaging/create-linux-packages.py $(VERSION)
#	env KUBERNAUT_VERSION=$(VERSION) packaging/upload-linux-packages.py $(VERSION)
    env KUBERNAUT_VERSION=$(VERSION) packaging/upload_packages.sh
