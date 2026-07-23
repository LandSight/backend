"""Topography metrics ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class TopographyMetricsId(EntityIdUUID6ValueObject):
    """Topography metrics ID value object using UUID6."""


__all__ = ("TopographyMetricsId",)
