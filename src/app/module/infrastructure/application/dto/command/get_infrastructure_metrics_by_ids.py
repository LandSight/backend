"""Get infrastructure metrics by IDs command."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.application.dto.command.category_metric_request import CategoryMetricRequest


@dataclass(frozen=True, slots=True)
class GetInfrastructureMetricsByIdsCommand:
    """Command for retrieving specific infrastructure metrics records by their IDs.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel the metrics belong to.
    current_user_id : UUID
        ID of the user performing the request.
    metrics : list[CategoryMetricRequest]
        Requested ``(category, metrics_id)`` references.
    """

    parcel_id: UUID
    current_user_id: UUID
    metrics: list[CategoryMetricRequest] = field(default_factory=list)


__all__ = ("GetInfrastructureMetricsByIdsCommand",)
