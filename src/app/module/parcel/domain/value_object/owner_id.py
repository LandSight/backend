"""Owner ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class OwnerId(EntityIdUUID6ValueObject):
    """Value object for a parcel owner's ID."""


__all__ = ("OwnerId",)
