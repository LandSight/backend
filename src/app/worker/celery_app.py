"""Celery application instance for the worker (CLI entrypoint)."""

from __future__ import annotations

from app.platform.celery import create_celery_app
from app.platform.config.loaders import load_redis_config


celery_app = create_celery_app(load_redis_config())
celery_app.conf.include = ["app.worker.tasks"]

__all__ = ("celery_app",)
