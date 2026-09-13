"""Metrics reader port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.module.shared.interface.internal import MetricsResponse


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object import AnalysisMetricRef


class MetricsReader(ABC):
    """Port for reading the metric values referenced by an analysis.

    Implementations:
    - :class:`app.module.analysis.infrastructure.reader.metrics_reader.MetricsReaderImpl`
    """

    @abstractmethod
    async def read(
        self,
        parcel_id: UUID,
        refs: list[AnalysisMetricRef],
        user_id: UUID,
    ) -> list[MetricsResponse]:
        """Read the neutral metrics responses behind the given references.

        Parameters
        ----------
        parcel_id : UUID
            ID of the parcel the metrics belong to.
        refs : list[AnalysisMetricRef]
            Metric references recorded for the analysis.
        user_id : UUID
            ID of the requesting user (for access validation).

        Returns
        -------
        list[MetricsResponse]
            Neutral metrics responses.
        """
        raise NotImplementedError


__all__ = ("MetricsReader", "MetricsResponse")
