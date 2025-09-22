.PHONY: install migrate collectstatic run dev build render-start

install:
	uv export --format=requirements.txt --quiet > requirements.txt
	uv pip install --system -r requirements.txt

migrate:
	uv run python manage.py migrate --noinput

collectstatic:
	uv run python manage.py collectstatic --noinput

run:
	uv run python manage.py runserver 0.0.0.0:8000

dev: install migrate
	$(MAKE) run

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:$$PORT
lint:
	uv run ruff check --fix
format:
	uv run ruff format