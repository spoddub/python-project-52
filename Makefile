.PHONY: build install collectstatic migrate start start-dev render-start lint format test

build:
	./build.sh

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate --noinput

start:
	uv run python manage.py runserver

start-dev:
	uv run python manage.py runserver --nostatic

render-start:
	uv run gunicorn task_manager.wsgi

lint:
	uv run ruff check --fix

format:
	uv run ruff format

test:
	uv run python manage.py test -v 2
