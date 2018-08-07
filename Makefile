# Makefile

.PHONY: test

BINARY_BASENAME := kubernaut
BINARY_OS       := linux
BINARY_PLATFORM := x86_64
BINARY_NAME     := $(BINARY_BASENAME)-$(BINARY_OS)-$(BINARY_PLATFORM)

all: test binary

clean:
	rm -rf \
		build \
		venv \
		.tox \
		*.egg-info \
		__pycache__ \
		.pytest_cache \
		ci-secrets.tar.gz
	find -iname "*.pyc" -delete

dev:
	pipenv install -e .

init:
	pipenv install --dev

test: init
	pipenv run py.test test

binary: test
	BINARY_NAME=$(BINARY_NAME) pipenv run tools/build-local.sh