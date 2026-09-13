"""Delete infrastructure metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.infrastructure.application.dto.command import DeleteInfrastructureMetricsCommand
from app.module.infrastructure.application.error import UnknownCategoryError
from app.module.infrastructure.domain.value_object import Category, InfrastructureMetricsId
from app.module.shared.application.use_case import BaseUseCase


if TYPE_CHECKING:
    from app.module.infrastructure.application.port import MetricsRepository


class DeleteInfrastructureMetricsUseCase(BaseUseCase[DeleteInfrastructureMetricsCommand, None]):
    """Delete infrastructure metrics snapshots by their ``(category, id)`` references.

    Used by owning modules (e.g. Analysis) to clean up snapshots they no longer
    reference.
    """

    def __init__(self, metrics_repository: MetricsRepository) -> None:
        self._metrics_repository = metrics_repository

    @override
    async def __call__(self, command: DeleteInfrastructureMetricsCommand) -> None:
        refs: list[tuple[Category, InfrastructureMetricsId]] = []
        for metric in command.metrics:
            try:
                category = Category(metric.category)
            except ValueError as exc:
                raise UnknownCategoryError(metric.category) from exc
            refs.append((category, InfrastructureMetricsId(metric.metrics_id)))

        await self._metrics_repository.delete(refs)


__all__ = ("DeleteInfrastructureMetricsUseCase",)
