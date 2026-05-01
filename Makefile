.PHONY: help install migrate test run celery beat docker-up docker-down clean

help:
	@echo "Django API Aggregator - Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make migrate     - Run database migrations"
	@echo "  make test        - Run tests"
	@echo "  make run         - Start development server"
	@echo "  make celery      - Start Celery worker"
	@echo "  make beat        - Start Celery beat"
	@echo "  make docker-up   - Start Docker services"
	@echo "  make docker-down - Stop Docker services"
	@echo "  make clean       - Clean up cache files"

install:
	pip install -r requirements/development.txt

migrate:
	python manage.py migrate

test:
	pytest

run:
	python manage.py runserver

celery:
	celery -A config worker -l info

beat:
	celery -A config beat -l info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
