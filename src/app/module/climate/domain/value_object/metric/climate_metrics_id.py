"""Climate metrics ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class ClimateMetricsId(EntityIdUUID6ValueObject):
    """Climate metrics ID value object using UUID6."""


__all__ = ("ClimateMetricsId",)
