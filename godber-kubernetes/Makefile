.DEFAULT_GOAL := help
.PHONY: help build push
SHELL := bash

IP ?= $(shell minikube ip)
ES_URL ?= http://$(IP):30200
IMAGE_NAME ?= starlette:1
NAMESPACE ?= default
LOG_LENGTH ?= 1000

help: ## show target summary
	@grep -E '^\S+:.* ## .+$$' $(MAKEFILE_LIST) | sed 's/##/#/' | while IFS='#' read spec help; do \
	  tgt=$${spec%%:*}; \
	  printf "\n%s: %s\n" "$$tgt" "$$help"; \
	  awk -F ': ' -v TGT="$$tgt" '$$1 == TGT && $$2 ~ "=" { print $$2 }' $(MAKEFILE_LIST) | \
	  while IFS='#' read var help; do \
	    printf "  %s  :%s\n" "$$var" "$$help"; \
	  done \
	done

build: webapp/Dockerfile ## builds docker images
	docker build -t $(IMAGE_NAME) ./webapp

push: ## push final docker image
	docker push $(IMAGE_NAME)

apply: ## deploy manifest to kubernetes
	kubectl apply -f ./manifest.yaml

clean: ## remove the kubernetes resources and docker image
	kubectl delete -f ./manifest.yaml && sleep 2 &&	docker rmi $(IMAGE_NAME)
