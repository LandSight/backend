"""Celery application factory.

Pure factory: builds a Celery app from a :class:`RedisConfig`. The consumer
entrypoint (``app.worker.celery_app``) owns the instance used by the Celery
CLI, while the HTTP layer gets one through DI.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from celery import Celery

from app.platform.outbox.constants import DRAIN_OUTBOX_TASK_NAME


if TYPE_CHECKING:
    from app.platform.config.models import RedisConfig


# Queue of the tasks sent without an explicit queue, notably the outbox relay.
# Every worker consumes it next to its own queue (``analysis`` or
# ``interpretation``, chosen by the module that enqueues the task), so the relay
# keeps running while all the workers of one kind are busy.
DEFAULT_QUEUE = "default"


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
    # Track started state so the logs show when a task actually begins running;
    # "received" only means the message was pulled from the broker and the task
    # may still be waiting behind other tasks on the worker.
    app.conf.task_track_started = True
    # Results are required: the metrics phase is a chord whose callback runs
    # only after every header task finishes.
    app.conf.task_ignore_result = False
    app.conf.result_expires = 3600
    app.conf.task_serializer = "json"
    app.conf.accept_content = ["json"]
    app.conf.result_serializer = "json"
    app.conf.timezone = "UTC"
    app.conf.enable_utc = True
    # Acknowledge messages only after the task body finishes, so a crashed or
    # restarted worker redelivers the message instead of losing it silently.
    app.conf.task_acks_late = True
    # Fetch one message at a time per worker process. Prevents one worker from
    # hoarding a backlog of relay tasks while a report task waits behind them.
    app.conf.worker_prefetch_multiplier = 1
    app.conf.task_default_queue = DEFAULT_QUEUE
    # Relay the transactional outbox. Runs on the Celery beat process alongside
    # the worker, so pending events are dispatched even if the producer crashed
    # after committing the state change.
    app.conf.beat_schedule = {
        "drain-outbox": {
            "task": DRAIN_OUTBOX_TASK_NAME,
            "schedule": 10.0,
        },
    }
    return app


__all__ = ("DEFAULT_QUEUE", "create_celery_app")
