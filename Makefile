IMAGE_NAME := quay.io/app-sre/manifest-bouncer
IMAGE_TAG := $(shell git rev-parse --short=7 HEAD)

ifneq (,$(wildcard $(CURDIR)/.docker))
	DOCKER_CONF := $(CURDIR)/.docker
else
	DOCKER_CONF := $(HOME)/.docker
endif

.PHONY: test
test:
	docker build -f dockerfiles/Dockerfile.test -t manifest-bouncer-test:latest .
	docker run manifest-bouncer-test:latest tox

.PHONY: build
build:
	@docker build -f dockerfiles/Dockerfil -t $(IMAGE_NAME):latest .
	@docker tag $(IMAGE_NAME):latest $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: push
push:
	@docker --config=$(DOCKER_CONF) push $(IMAGE_NAME):latest
	@docker --config=$(DOCKER_CONF) push $(IMAGE_NAME):$(IMAGE_TAG)
