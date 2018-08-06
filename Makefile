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

compile: SKIP_TESTS = false
compile: DOCKER_WORKDIR = /work
compile: DOCKER_ARGS += -e BINARY_NAME=$(BINARY_NAME)
compile: DOCKER_ARGS += -e SKIP_TESTS=$(SKIP_TESTS)
compile:
	$(DOCKER_RUN) $(DOCKER_MOUNTDIR)/tools/build-docker.sh
	cp build/out/$(BINARY_NAME) build/out/$(BINARY_BASENAME)

dev:
	pipenv install -e .

init:
	pipenv install --dev

test: init
	pipenv run py.test test

binary: test
	BINARY_NAME=$(BINARY_NAME) tools/build-local.sh