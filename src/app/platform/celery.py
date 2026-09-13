"""Celery application factory.

Pure factory: builds a Celery app from a :class:`RedisConfig`. The consumer
entrypoint (``app.worker.celery_app``) owns the instance used by the Celery
CLI, while the HTTP layer gets one through DI.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from celery import Celery


if TYPE_CHECKING:
    from app.platform.config.models import RedisConfig


def create_celery_app(redis_config: RedisConfig) -> Celery:
    """Create a Celery application configured from Redis settings.

    Parameters
    ----------
    redis_config : RedisConfig
        Redis configuration used as the broker and result backend.

    Returns
    -------
    Celery
        Configured Celery application.
    """
    broker_url = redis_config.get_url()

    app = Celery("landsight")
    app.conf.broker_url = broker_url
    app.conf.result_backend = broker_url
    # Results are required: the metrics phase is a chord whose callback runs
    # only after every header task finishes.
    app.conf.task_ignore_result = False
    app.conf.result_expires = 3600
    app.conf.task_serializer = "json"
    app.conf.accept_content = ["json"]
    app.conf.result_serializer = "json"
    app.conf.timezone = "UTC"
    app.conf.enable_utc = True
    return app


__all__ = ("create_celery_app",)
