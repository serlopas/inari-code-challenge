#!make
.DEFAULT_GOAL=up

build:
	docker-compose build

up:
	docker-compose -f docker-compose.yml up --build --detach

down:
	docker-compose -f docker-compose.yml stop
