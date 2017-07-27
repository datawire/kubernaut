.PHONY: default release

VERSION=$(shell git describe --tags)
SHELL:=/bin/bash

default:
	@echo "See http://kubernaut.io/additional-information/developing.html"

version:
	@echo $(VERSION)

## Setup dependencies ##

virtualenv:
	virtualenv --python=python3 virtualenv
	virtualenv/bin/pip install -Ur requirements.txt

## Development ##

## Release ##

# Will be run in Travis CI on tagged commits
release: virtualenv
	env KUBERNAUT_VERSION=$(VERSION) packaging/homebrew-package.sh
	packaging/create-linux-packages.py $(VERSION)
	packaging/upload-linux-packages.py $(VERSION)
