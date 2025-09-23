.PHONY: install install-local migrate collectstatic run dev build render-start lint format test

install:
	uv export --format=requirements.txt --quiet > requirements.txt
	uv pip install --system -r requirements.txt

migrate:
	uv run python manage.py migrate --noinput

collectstatic:
	uv run python manage.py collectstatic --noinput

install-local:
	uv venv --clear
	uv pip install --python .venv/bin/python -r requirements.txt

run:
	uv run python manage.py runserver 0.0.0.0:8000

dev: install-local migrate
	$(MAKE) run

# ==== Обёртки ====
build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:$$PORT

lint:
	uv run ruff check --fix
format:
	uv run ruff format
test:
	uv run python manage.py test -v 2