"""Delete infrastructure metrics command."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.application.dto.command.category_metric_request import CategoryMetricRequest


@dataclass(frozen=True, slots=True)
class DeleteInfrastructureMetricsCommand:
    """Command for deleting infrastructure metrics snapshots by their references."""

    metrics: list[CategoryMetricRequest] = field(default_factory=list)


__all__ = ("DeleteInfrastructureMetricsCommand",)
