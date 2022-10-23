.PHONY: help

.DEFAULT_GOAL := help
runner=$(shell whoami)

PROJECTNAME := UltimateAudioBot
PI_TAG_BOT := pi4-02:5000/ultimate_bot:pi
PI_TAG_BACKEND := pi4-02:5000/ultimate_bot_backend:pi

help: ## This is the help command.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the docker image
	docker-compose build
up: ## Run the docker container
	docker-compose up

build-up: build up ## Build and run the docker container

build-prod: ## Build the docker image for production
	docker-compose -f docker-compose_prod-test.yml build

up-prod: ## Run the docker container for production
	docker-compose -f docker-compose_prod-test.yml up

build-up-prod: build-prod up-prod ## Build and run the docker container for production

down: ## Stop the docker container
	docker-compose down

down-prod: ## Stop the docker container for production
	docker-compose -f docker-compose_prod-test.yml down

down-all: down down-prod ## Stop all docker containers

build-pi: build-pi-bot build-pi-backend ## Build the docker image for pi

build-pi-backend: ## Build the docker backend image for raspberry pi
	docker buildx build --platform=linux/arm64  -f ./backend/docker/Dockerfile --network=host -t $(PI_TAG_BACKEND) ./backend


build-pi-bot: ## Build the docker bot image for raspberry pi
	docker buildx build --platform=linux/arm64  -f ./bot/docker-compose/Dockerfile --network=host -t $(PI_TAG_BOT) ./

clear-pycache: ## Clear all pycache files
	find -type d -name "__pycache__" ! -path './venv*' -exec sudo rm -rf {} \;