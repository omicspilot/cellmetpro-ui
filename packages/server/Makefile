.PHONY: dev check test serve clean

# First-time setup: install dev dependencies and git hooks
dev:
	uv sync --extra dev
	pre-commit install

# Run the full quality pass (mirrors the uv_clean_code alias)
check:
	uv run mypy .
	uv run ruff check --fix .
	uv run ruff format .

# Run the test suite
test:
	uv run pytest tests

# Start the development server
serve:
	uv run cellmetpro-server

# Remove the virtual environment (re-run `make dev` to rebuild)
clean:
	rm -rf .venv
