.PHONY: help install migrate run test lint shell superuser

help:
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@echo "  install    Install dependencies"
	@echo "  migrate    Run database migrations"
	@echo "  makemigrations  Create new migrations"
	@echo "  run        Start development server"
	@echo "  test       Run tests"
	@echo "  shell      Open Django shell"
	@echo "  superuser  Create superuser"

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

run:
	python manage.py runserver

test:
	python manage.py test

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser
