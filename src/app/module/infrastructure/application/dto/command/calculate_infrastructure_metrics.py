"""Calculate infrastructure metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.application.dto.command.category_request import CategoryRequest


@dataclass(frozen=True, slots=True)
class CalculateInfrastructureMetricsCommand:
    """Command for calculating infrastructure metrics for a parcel.

    Computes metrics for a variadic set of categories, each with its own
    buffer radius, in a single request. The parcel geometry is fetched
    internally (from the Parcel module) rather than supplied by the caller.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel to calculate metrics for.
    current_user_id : UUID
        ID of the user performing the calculation.
    categories : list[CategoryRequest]
        Requested categories with their buffer radii.
    """

    parcel_id: UUID
    current_user_id: UUID
    categories: list[CategoryRequest]


__all__ = ("CalculateInfrastructureMetricsCommand",)
