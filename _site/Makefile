# Makefile to manage Docker/Jekyll for this project
# Usage: make <target>

SHELL := /bin/bash
.DEFAULT_GOAL := help

COMPOSE = docker compose
COMPOSE_LOCAL = docker compose -f docker-local.yml
CONTAINER = al-folio-website
CONTAINER_LOCAL = al-folio-local-website
IMAGE = al-folio-local-docker
PORT ?= 8080

.PHONY: help build compose-build up up-local down down-local logs logs-local enter enter-local clean ps status

help:
	@echo "Makefile targets:"
	@echo "  make build           - docker build image (uses Dockerfile)"
	@echo "  make compose-build   - docker-compose build (docker-local.yml)"
	@echo "  make up              - start site with prebuilt image (docker-compose.yml)"
	@echo "  make up-local        - build image and start using docker-local.yml"
	@echo "  make down            - stop services (docker-compose.yml)"
	@echo "  make down-local      - stop services (docker-local.yml)"
	@echo "  make logs            - follow logs (docker-compose.yml)"
	@echo "  make logs-local      - follow logs (docker-local.yml)"
	@echo "  make enter           - bash into running prebuilt container"
	@echo "  make enter-local     - bash into running local container"
	@echo "  make clean           - remove Gemfile.lock and _site/"
	@echo "  make ps              - show docker-compose ps"
	@echo "  make status          - docker ps filtered for al-folio containers"

build:
	@echo "Building image $(IMAGE)..."
	docker build -t $(IMAGE) .

compose-build:
	@echo "Running docker-compose build (docker-local.yml)..."
	$(COMPOSE_LOCAL) build

up:
	@echo "Starting site from prebuilt image (docker-compose.yml) on port $(PORT)..."
	$(COMPOSE) up --remove-orphans --force-recreate -d

up-local:
	@echo "Building image and starting local container (docker-local.yml) on port $(PORT)..."
	$(COMPOSE_LOCAL) up --build --remove-orphans --force-recreate -d

down:
	@echo "Stopping services (docker-compose.yml)..."
	$(COMPOSE) down

down-local:
	@echo "Stopping services (docker-local.yml)..."
	$(COMPOSE_LOCAL) down

logs:
	$(COMPOSE) logs -f

logs-local:
	$(COMPOSE_LOCAL) logs -f

enter:
	@echo "Entering container $(CONTAINER)..."
	docker exec -it $(CONTAINER) /bin/bash || docker exec -it $(CONTAINER) /bin/sh

enter-local:
	@echo "Entering container $(CONTAINER_LOCAL)..."
	docker exec -it $(CONTAINER_LOCAL) /bin/bash || docker exec -it $(CONTAINER_LOCAL) /bin/sh

clean:
	@echo "Cleaning Gemfile.lock and _site/ ..."
	-rm -f Gemfile.lock
	-rm -rf _site

ps:
	$(COMPOSE) ps

status:
	docker ps --filter "name=al-folio" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
