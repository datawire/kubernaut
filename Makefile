# Makefile

.SHELL: bash
.PHONY: build init test publish

DATE        = $(shell date --utc +%Y.%m.%d)
GIT_COMMIT  = $(shell git rev-parse --short --verify HEAD)
DATE_COMMIT = $(DATE)-$(COMMIT)

BINARY_BASENAME = kubernaut
BINARY_PLATFORM = amd64
BINARY_NAME = $(BINARY_BASENAME)-$(BINARY_OS)-$(BINARY_PLATFORM)

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

smoketest:
	build/out/$(shell cat version.txt)/$(BINARY_OS)/$(BINARY_PLATFORM)/kubernaut --version

binary:
	printf "$(DATE)-$(GIT_COMMIT)" > version.txt
	pipenv run pyinstaller kubernaut/cli.py \
	--distpath "build/out/$(DATE)-$(GIT_COMMIT)/$(BINARY_OS)/$(BINARY_PLATFORM)" \
	--add-data ../version.txt:kubernaut/ \
	--name $(BINARY_BASENAME) \
	--onefile \
	--specpath "build/" \
	--workpath "build/work"

publish:
	gsutil cp -n -r build/out/* gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)
	gsutil cp version.txt gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)/latest.txt

release:
	@ if ! gsutil -q stat gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)/$(VERSION)/linux/amd64/kubernaut; then \
		echo "VERSION: '$(VERSION)' not found! Was it previously published?"; \
		exit 1; \
	fi

	gsutil cp  -R \
		gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)/$(VERSION)/* \
		gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)/$(shell printf "$(VERSION)" | cut -d '-' -f 1)/

	printf "$(shell printf "$(VERSION)" | cut -d '-' -f 1)" > stable.txt
	gsutil cp stable.txt gs://$(GCS_RELEASE_BUCKET_NAME)/$(BINARY_BASENAME)/stable.txt
