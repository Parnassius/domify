.PHONY: format
format:
	@uv run ruff check src --fix-only
	@uv run ruff format src

.PHONY: format-check
format-check:
	@uv run ruff format src --check

.PHONY: mypy
mypy:
	@uv run mypy src

.PHONY: ruff
ruff:
	@uv run ruff check src

.PHONY: lint
lint: format-check mypy ruff

.PHONY: all
all: format mypy ruff

.DEFAULT_GOAL := all
