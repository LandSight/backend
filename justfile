set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := true

VENV_DIR := ".venv"
BUILD_DIR := "build"
CACHE_DIR := ".cache"
DOCS_HOST := env_var_or_default("DOCS_HOST", "127.0.0.1")
DOCS_PORT := env_var_or_default("DOCS_PORT", "8008")

default:
    @just --list

install:
    @uv venv {{ VENV_DIR }}
    @uv sync
    @uv run --group=pre-commit pre-commit install

clean:
    @find -type d -name "dist" -exec rm -rf {} +
    @find -type d -name "{{ BUILD_DIR }}" -exec rm -rf {} +
    @find -type d -name "{{ CACHE_DIR }}" -exec rm -rf {} +
    @find -type d -name "__pycache__" -exec rm -rf {} +
    @find -type d -name "*.egg-info" -exec rm -rf {} +
    @find -type f -name ".coverage" -exec rm -rf {} +
    @find -type f -name "*,cover" -exec rm -rf {} +
    @find -type f -name "*~" -exec rm -rf {} +
    @find -type f -name "*.egg" -exec rm -rf {} +

upgrade:
    @uv lock --upgrade
    @uv run --group=pre-commit pre-commit autoupdate

lock:
    @uv lock

test:
    @uv run --group=test pytest --cov=src/app --cov-report=term-missing --cov-append

lint:
    @uv run --group=lint ty check
    @uv run --group=lint ruff format --preview --check
    @uv run --group=lint ruff check --show-fixes --preview

fmt:
    @uv run --group=lint ruff format --preview

pre-commit:
    @uv run --group=pre-commit pre-commit run

check: fmt lint test pre-commit

docs-build:
    @uv run --group=docs mkdocs build

docs-serve:
    @uv run --group=docs mkdocs serve --dev-addr="{{ DOCS_HOST }}:{{ DOCS_PORT }}" --no-livereload

changelog-build:
    @uv run --group=changelog towncrier build

changelog-fragment:
    @uv run --group=changelog towncrier create
