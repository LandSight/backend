"""Get infrastructure metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.application.dto.command.category_request import CategoryRequest


@dataclass(frozen=True, slots=True)
class GetInfrastructureMetricsCommand:
    """Command for getting infrastructure metrics for a parcel.

    Gets metrics for a variadic set of categories, each with its own
    buffer radius, in a single request.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel of calculated metrics.
    categories : list[CategoryRequest]
        Requested categories with their buffer radii.
    """

    parcel_id: UUID
    categories: list[CategoryRequest]


__all__ = ("GetInfrastructureMetricsCommand",)
