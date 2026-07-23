set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := true

VENV_DIR := ".venv"
BUILD_DIR := "build"
CACHE_DIR := ".cache"
SRC_DIR := "src"

APP_HOST := env("APP_HOST", "127.0.0.1")
APP_PORT := env("APP_PORT", "8000")
DOCS_HOST := env("DOCS_HOST", "127.0.0.1")
DOCS_PORT := env("DOCS_PORT", "8008")

COMPOSE_CMD := env("COMPOSE_CMD", "docker-compose")


default:
    @just --list

# ── Environment ──────────────────────────────────────────────────────

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

# ── Dependencies ─────────────────────────────────────────────────────

upgrade:
    @uv lock --upgrade
    @uv run --group="git-hooks" prek auto-update

lock:
    @uv lock

# ── Quality ──────────────────────────────────────────────────────────

test:
    @uv run --group="test" pytest

lint:
    @uv run --group="lint" ty check
    @uv run --group="lint" ruff format --preview --check
    @uv run --group="lint" ruff check --show-fixes --preview

fmt:
    @uv run --group="lint" ruff format --preview

check: fmt lint test

# ── Documentation ────────────────────────────────────────────────────

docs-build:
    @uv run --group="docs" zensical build

docs-serve:
    @uv run --group="docs" zensical serve --dev-addr="{{ DOCS_HOST }}:{{ DOCS_PORT }}"

# ── Changelog ────────────────────────────────────────────────────────

changelog-build:
    @uv run --group="changelog" towncrier build

changelog-fragment:
    @uv run --group="changelog" towncrier create

# ── Docker / Podman ──────────────────────────────────────────────────

# Start all infrastructure services (PostgreSQL + Redis)
up:
    @{{ COMPOSE_CMD }} up --detach --wait

# Stop all infrastructure services
down:
    @{{ COMPOSE_CMD }} down

# Start only PostgreSQL
db-up:
    @{{ COMPOSE_CMD }} up --detach --wait postgres

# Stop only PostgreSQL
db-down:
    @{{ COMPOSE_CMD }} stop postgres

# View service logs
logs:
    @{{ COMPOSE_CMD }} logs --follow

# ── Module Migrations ────────────────────────────────────
# Uses a single global alembic.ini with named sections.
# Usage: just migration-create <module> "<description>"
#        just migration-upgrade <module>
#        just migration-downgrade <module> <steps>

migration-create module description:
    @uv run alembic -n {{ module }} revision --autogenerate -m "{{ description }}"

migration-upgrade module:
    @uv run alembic -n {{ module }} upgrade head

migration-downgrade module steps:
    @uv run alembic -n {{ module }} downgrade -{{ steps }}

migration-current module:
    @uv run alembic -n {{ module }} current

migration-history module:
    @uv run alembic -n {{ module }} history

# ── Application ──────────────────────────────────────────────────────

# Run the application locally with hot-reload
app-serve:
    @uv run --group="dev" granian \
        --host="{{ APP_HOST }}" \
        --port="{{ APP_PORT }}" \
        --interface="asgi" \
        --factory \
        --reload \
        --reload-paths="{{ SRC_DIR }}" \
        app.interface.http.asgi:create_asgi_application
