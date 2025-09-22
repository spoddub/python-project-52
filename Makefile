lint:
	uv run ruff check --fix
	uv run ruff format
build:
	./build.sh
render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:$$PORT