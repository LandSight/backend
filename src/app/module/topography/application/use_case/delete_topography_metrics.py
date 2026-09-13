"""Delete topography metrics use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.shared.application.use_case import BaseUseCase
from app.module.topography.application.dto.command import DeleteTopographyMetricsCommand


if TYPE_CHECKING:
    from app.module.topography.application.port import MetricsRepository


class DeleteTopographyMetricsUseCase(BaseUseCase[DeleteTopographyMetricsCommand, None]):
    """Delete topography metrics snapshots by their IDs.

    Used by owning modules (e.g. Analysis) to clean up snapshots they no longer
    reference.
    """

    def __init__(self, metrics_repository: MetricsRepository) -> None:
        self._metrics_repository = metrics_repository

    @override
    async def __call__(self, command: DeleteTopographyMetricsCommand) -> None:
        await self._metrics_repository.delete(command.metrics_ids)


__all__ = ("DeleteTopographyMetricsUseCase",)
