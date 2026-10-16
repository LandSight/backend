"""Restriction gateway backed by the restriction module's Internal API.

Translates the module's internal results into the analysis value objects, so
nothing of the restriction module's contract reaches the analysis domain.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import RestrictionService
from app.module.analysis.domain.value_object.restriction import RestrictionCheck, RestrictionCheckRef, RestrictionHit
from app.module.restriction.interface.internal.dto import (
    CalculateCheckInput,
    DeleteChecksInput,
    GetCheckInput,
)
from app.module.shared.domain.value_object import Area, Share


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.restriction.interface.internal.port import RestrictionInternalAPI


class RestrictionServiceImpl(RestrictionService):
    """Calculates, gets and deletes restriction checks through the restriction module."""

    def __init__(self, restriction_api: RestrictionInternalAPI) -> None:
        self._restriction_api = restriction_api

    @override
    async def calculate(self, parcel_id: UUID, user_id: UUID) -> RestrictionCheckRef:
        """See :class:`app.module.analysis.application.port.RestrictionService.calculate`."""
        check = await self._restriction_api.calculate_check(
            CalculateCheckInput(parcel_id=parcel_id, current_user_id=user_id),
        )
        return RestrictionCheckRef(check_id=check.id)

    @override
    async def get(self, ref: RestrictionCheckRef, user_id: UUID) -> RestrictionCheck:
        """See :class:`app.module.analysis.application.port.RestrictionService.get`."""
        check = await self._restriction_api.get_check(GetCheckInput(check_id=ref.check_id, current_user_id=user_id))
        return RestrictionCheck(
            ref=ref,
            hits=tuple(
                RestrictionHit(
                    kind=hit.kind,
                    overlap_area=Area(hit.overlap_area_m2),
                    overlap_share=Share(hit.overlap_share),
                    zone_names=tuple(hit.zone_names),
                    legal_basis=hit.legal_basis,
                )
                for hit in check.hits
            ),
        )

    @override
    async def delete(self, refs: list[RestrictionCheckRef], user_id: UUID) -> None:
        """See :class:`app.module.analysis.application.port.RestrictionService.delete`."""
        if not refs:
            return
        await self._restriction_api.delete_checks(
            DeleteChecksInput(check_ids=[ref.check_id for ref in refs], current_user_id=user_id),
        )


__all__ = ("RestrictionServiceImpl",)
