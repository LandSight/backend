"""Restriction check entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.restriction.domain.value_object import RestrictionCheckId
from app.module.shared.domain.entity import BaseEntity
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    import datetime

    from app.module.restriction.domain.value_object import ParcelId, RestrictionHit
    from app.module.shared.domain.value_object import SemanticVersion


class RestrictionCheck(BaseEntity[RestrictionCheckId]):
    """Snapshot of the restriction zones that overlap a parcel.

    Attributes
    ----------
    id : RestrictionCheckId
        Unique identifier for this check.
    parcel_id : ParcelId
        ID of the checked parcel.
    hits : tuple[RestrictionHit, ...]
        One entry per overlapping zone kind; empty when the parcel is clear.
    rules_version : SemanticVersion
        Version of the zone rules the zones were built with, so a stored
        check can be traced to the widths in force when it was made.
    created_at : datetime | None
        When the check was made (UTC); ``None`` if not yet persisted.
    """

    def __init__(
        self,
        id: RestrictionCheckId,
        parcel_id: ParcelId,
        hits: tuple[RestrictionHit, ...],
        rules_version: SemanticVersion,
        created_at: datetime.datetime | None = None,
    ) -> None:
        self._parcel_id = parcel_id
        self._hits = hits
        self._rules_version = rules_version
        self._created_at = created_at

        super().__init__(id)

    @override
    def _validate(self) -> None:
        kinds = [hit.kind for hit in self._hits]
        if len(kinds) != len(set(kinds)):
            message = "A restriction check must hold at most one hit per zone kind."
            raise ValidationError(message)

    @property
    def parcel_id(self) -> ParcelId:
        """ID of the checked parcel."""
        return self._parcel_id

    @property
    def hits(self) -> tuple[RestrictionHit, ...]:
        """Overlapping zone kinds."""
        return self._hits

    @property
    def rules_version(self) -> SemanticVersion:
        """Version of the zone rules the zones were built with."""
        return self._rules_version

    @property
    def created_at(self) -> datetime.datetime | None:
        """When the check was made (UTC)."""
        return self._created_at


__all__ = ("RestrictionCheck",)
