.PHONY: format
format:
	@uv run ruff check src tests --fix-only
	@uv run ruff format src tests

.PHONY: format-check
format-check:
	@uv run ruff format src tests --check

.PHONY: darglint
darglint:
	@uv run darglint src tests -v 2

.PHONY: mypy
mypy:
	@uv run mypy src tests

.PHONY: ruff
ruff:
	@uv run ruff check src tests

.PHONY: pytest
pytest:
	@uv run pytest --cov

.PHONY: lint
lint: format-check darglint mypy ruff

.PHONY: all
all: format darglint mypy ruff pytest

.DEFAULT_GOAL := all
