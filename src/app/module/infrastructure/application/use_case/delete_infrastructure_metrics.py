"""Delete infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.dto.command import DeleteInfrastructureMetricsCommand
from app.module.infrastructure.application.error import UnknownCategoryError
from app.module.infrastructure.domain.value_object import (
    Category,
    InfrastructureMetricsId,
    MetricFamily,
    family_of,
)
from app.module.shared.application.use_case import BaseUseCase


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from app.module.infrastructure.application.port import MetricsRepository


class DeleteInfrastructureMetricsUseCase(BaseUseCase[DeleteInfrastructureMetricsCommand, None]):
    """Delete infrastructure metrics by their ``(category, id)`` references.

    Used by owning modules (e.g. Analysis) to clean up snapshots they no longer
    reference.
    """

    def __init__(self, metrics_repository: MetricsRepository) -> None:
        self._metrics_repository = metrics_repository
        self._handlers: dict[
            MetricFamily,
            Callable[[list[InfrastructureMetricsId]], Awaitable[None]],
        ] = {
            MetricFamily.FACILITY: metrics_repository.delete_facility,
            MetricFamily.ECOLOGY: metrics_repository.delete_ecology,
            MetricFamily.UTILITY: metrics_repository.delete_utility,
            MetricFamily.ROAD_ACCESSIBILITY: metrics_repository.delete_road_accessibility,
            MetricFamily.GEOGRAPHIC_POSITION: metrics_repository.delete_geographic_position,
        }

    @override
    async def __call__(self, command: DeleteInfrastructureMetricsCommand) -> None:
        grouped: dict[MetricFamily, list[InfrastructureMetricsId]] = {}
        for metric in command.metrics:
            try:
                category = Category(metric.category)
            except ValueError as exc:
                raise UnknownCategoryError(metric.category) from exc
            grouped.setdefault(family_of(category), []).append(InfrastructureMetricsId(metric.metrics_id))

        for family, metrics_ids in grouped.items():
            await self._handlers[family](metrics_ids)


__all__ = ("DeleteInfrastructureMetricsUseCase",)
