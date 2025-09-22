lint:
	uv run ruff check --fix
	uv run ruff format
build:
	./build.sh