# Makefile

.PHONY: build init test publish

GIT_COMMIT=$(shell git rev-parse --short --verify HEAD)

BINARY_BASENAME = kubernaut
BINARY_PLATFORM = amd64
BINARY_NAME = $(BINARY_BASENAME)-$(BINARY_OS)-$(BINARY_PLATFORM)
BINARY_NAME_VERSIONED = $(BINARY_BASENAME)-$(GIT_COMMIT)-$(BINARY_OS)-$(BINARY_PLATFORM)

GCS_RELEASE_BUCKET_NAME = releases.datawire.io

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
		.mypy_cache \
		.pytest_cache \
		ci-secrets.tar.gz \
		kubernaut*.spec
	find -iname "*.pyc" -delete
	pipenv clean

dev:
	pipenv install -e .

init:
	pipenv install --dev

test: init
	pipenv run py.test test

binary: test
	pipenv run pyinstaller kubernaut/cli.py \
	--distpath "build/out/$(GIT_COMMIT)/$(BINARY_OS)/$(BINARY_PLATFORM)" \
	--name $(BINARY_BASENAME) \
	--onefile \
	--specpath "build/" \
	--workpath "build/work"

publish:
	printf "$(GIT_COMMIT)" > build/latest.txt
	gsutil cp -r build/out/*   gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)
	gsutil cp build/latest.txt gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)/latest.txt
