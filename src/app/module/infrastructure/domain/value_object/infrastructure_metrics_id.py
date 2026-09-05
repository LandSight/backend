"""Infrastructure metrics ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class InfrastructureMetricsId(EntityIdUUID6ValueObject):
    """Infrastructure metrics ID value object using UUID6."""


__all__ = ("InfrastructureMetricsId",)
