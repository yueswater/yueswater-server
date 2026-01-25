.PHONY: help install shell run migrations migrate superuser format lint check clean tree \
        docker-up docker-down docker-logs docker-shell docker-migrate \
        docker-makemigrations docker-superuser docker-restart docker-clean

help:
	@make -qp | awk -F':' '/^[a-zA-Z0-9_-]+:$$/ {print $$1}' | sort

install:
	poetry install

shell:
	poetry shell

run:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8

check:
	make format
	make lint

clean:
	rm -rf .venv
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

tree:
	tree -I "migrations|__pycache__|logs"

# Docker commands
docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec web /bin/bash

docker-migrate:
	docker-compose exec web python manage.py migrate

docker-makemigrations:
	docker-compose exec web python manage.py makemigrations

docker-superuser:
	docker-compose exec web python manage.py createsuperuser

docker-restart:
	docker-compose restart web

docker-clean:
	docker-compose down --volumes --rmi all