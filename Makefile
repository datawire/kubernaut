# Makefile

.PHONY: init test

GIT_COMMIT=$(shell git rev-parse --short --verify HEAD)

BINARY_BASENAME = kubernaut
BINARY_PLATFORM = x86_64
BINARY_NAME = $(BINARY_BASENAME)-$(GIT_COMMIT)-$(BINARY_OS)-$(BINARY_PLATFORM)

ifeq ($(OS),Windows_NT)
	BINARY_OS = windows
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		BINARY_OS = linux
	endif
	ifeq ($(UNAME_S),Darwin)
		BINARY_OS = darwin
	endif
endif

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