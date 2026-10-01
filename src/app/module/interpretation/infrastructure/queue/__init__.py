"""Interpretation task queues."""

from __future__ import annotations

from .celery_interpretation_task_queue import (
    PROCESS_INTERPRETATION_TASK_NAME,
    CeleryInterpretationTaskQueue,
)


__all__ = ("PROCESS_INTERPRETATION_TASK_NAME", "CeleryInterpretationTaskQueue")
