# Базовый образ
FROM python:3.14.2-slim-trixie AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app

# Бинарь uv из официального образа Astral
FROM ghcr.io/astral-sh/uv:0.9.18 AS uvbin

# Сборщик зависимостей/приложения
FROM base AS builder

# Можно переключать набор зависимостей:
# - prod: "--no-dev" (по умолчанию)
# - dev:  "--group dev"
ARG UV_SYNC_ARGS="--no-dev"

COPY --from=uvbin /uv /usr/local/bin/uv

# Если появятся зависимости с нативными расширениями — добавьте нужные build deps здесь.
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# 1) Ставим только зависимости без самого проекта
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync ${UV_SYNC_ARGS} --no-install-project --frozen

# 2) Кладём исходники
COPY src ./src

# 3) Ставим проект и, при необходимости, dev-группы
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync ${UV_SYNC_ARGS} --frozen

# Рантайм-образ
FROM base AS runtime
COPY --from=builder /app /app

# По умолчанию, но в compose мы обычно переопределяем command и порт
EXPOSE 8000
CMD ["granian", "--host", "0.0.0.0", "--port", "8000", "--interface", "asgi", "--factory", "app.interface.http.asgi:create_asgi_application"]
