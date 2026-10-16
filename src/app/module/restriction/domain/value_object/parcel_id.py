"""Parcel ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class ParcelId(EntityIdUUID6ValueObject):
    """Parcel identifier for restriction checks."""


__all__ = ("ParcelId",)
