.PHONY=build run prep_env clean_image up down ps top

PIP=python3 -m pip
DOCKERCOMPOSE:=$(shell which docker-compose 2>/dev/null || echo "docker compose")

include .env
-include .env.local

help:
	@echo "build: Build base image for docker"
	@echo "run: To create a new container from image $(IMG)"
	@echo "clean_image: clear old dangling images to save space"
	@echo "build: build according to docker-compose.yaml"
	@echo "up: run the services according to docker-compose.yaml"

TEMP_ENV := .env

IMG := dev/airflow_extension

build: clean_image prep_env
	sudo docker build . -t dev/airflow_extension
	@echo "Base image built"

prep_env: .env
	@cat .env > ${TEMP_ENV}
	@echo "" >> ${TEMP_ENV}
	-@cat .env.local >> ${TEMP_ENV}
	@echo Created temp env ${TEMP_ENV}

clean_image: prep_env
	sudo docker image prune -f

up:
	sudo ${DOCKERCOMPOSE} --env-file ${TEMP_ENV} up -d

down: 
	sudo ${DOCKERCOMPOSE} --env-file ${TEMP_ENV} down 

ps:
	sudo ${DOCKERCOMPOSE} ps

top:
	sudo ${DOCKERCOMPOSE} top