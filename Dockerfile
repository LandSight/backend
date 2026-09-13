# Development image for the LandSight backend (API + Celery worker).
#
# Based on Ubuntu 24.04 so the system GDAL (3.8.x) matches the pinned
# `gdal==3.8.4` dependency. Python 3.14 is installed via uv.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        gdal-bin \
        libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN uv python install 3.14

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "granian", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--interface", "asgi", \
     "--factory", \
     "app.interface.http.asgi:create_asgi_application"]
