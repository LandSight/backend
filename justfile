set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := true

VENV_DIR := ".venv"
BUILD_DIR := "build"
CACHE_DIR := ".cache"

APP_HOST := env("APP_HOST", "127.0.0.1")
APP_PORT := env("APP_PORT", "8000")
DOCS_HOST := env("DOCS_HOST", "127.0.0.1")
DOCS_PORT := env("DOCS_PORT", "8008")

default:
    @just --list

venv:
    @uv venv {{ VENV_DIR }}

sync:
    @uv sync --all-extras --all-groups

setup: venv sync
    @uv run --group="git-hooks" prek install

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
    @uv run --group="git-hooks" prek auto-update

lock:
    @uv lock

test:
    @uv run --group="test" pytest

lint:
    @uv run --group="lint" ty check
    @uv run --group="lint" ruff format --preview --check
    @uv run --group="lint" ruff check --show-fixes --preview

fmt:
    @uv run --group="lint" ruff format --preview

check: fmt lint test

docs-build:
    @uv run --group="docs" mkdocs build

docs-serve:
    @uv run --group="docs" mkdocs serve --dev-addr="{{ DOCS_HOST }}:{{ DOCS_PORT }}" --no-livereload

changelog-build:
    @uv run --group="changelog" towncrier build

changelog-fragment:
    @uv run --group="changelog" towncrier create

app-serve:
    @uv run --group="dev" granian \
        --host="{{ APP_HOST }}" \
        --port="{{ APP_PORT }}" \
        --interface="asgi" \
        --factory \
        --reload \
        app.interface.http.asgi:create_asgi_application
