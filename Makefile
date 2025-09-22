.PHONY: install migrate collectstatic run dev build render-start

install:
	uv export --format=requirements --quiet > requirements.txt
	uv pip install --system -r requirements.txt

migrate:
	python manage.py migrate --noinput

collectstatic:
	python manage.py collectstatic --noinput

run:
	python manage.py runserver 0.0.0.0:8000

dev: install migrate
	$(MAKE) run

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:$$PORT
lint:
	uv run ruff check --fix
format:
	uv run ruff format