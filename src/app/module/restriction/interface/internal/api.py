"""Concrete implementation of the Restriction module's internal API.

See :class:`app.module.restriction.interface.internal.port.RestrictionInternalAPI`
for the abstract interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.restriction.application.dto.command import (
    CheckParcelRestrictionsCommand,
    DeleteRestrictionChecksCommand,
    GetRestrictionCheckCommand,
)
from app.module.restriction.interface.internal.dto import RestrictionCheckResult, RestrictionHitResult
from app.module.restriction.interface.internal.port import RestrictionInternalAPI


if TYPE_CHECKING:
    from app.module.restriction.application.dto.response import RestrictionCheckResponse
    from app.module.restriction.application.use_case import (
        CheckParcelRestrictionsUseCase,
        DeleteRestrictionChecksUseCase,
        GetRestrictionCheckUseCase,
    )
    from app.module.restriction.interface.internal.dto import (
        CheckRestrictionsInput,
        DeleteChecksInput,
        GetCheckInput,
    )


class RestrictionInternal(RestrictionInternalAPI):
    """Concrete implementation of the Restriction internal API."""

    def __init__(
        self,
        check_restrictions_use_case: CheckParcelRestrictionsUseCase,
        get_check_use_case: GetRestrictionCheckUseCase,
        delete_checks_use_case: DeleteRestrictionChecksUseCase,
    ) -> None:
        self._check_restrictions = check_restrictions_use_case
        self._get_check = get_check_use_case
        self._delete_checks = delete_checks_use_case

    @override
    async def check_restrictions(self, input_data: CheckRestrictionsInput) -> RestrictionCheckResult:
        """See :meth:`RestrictionInternalAPI.check_restrictions`."""
        result = await self._check_restrictions(
            CheckParcelRestrictionsCommand(
                parcel_id=input_data.parcel_id,
                current_user_id=input_data.current_user_id,
            )
        )
        return self._to_result(result)

    @override
    async def get_check(self, input_data: GetCheckInput) -> RestrictionCheckResult:
        """See :meth:`RestrictionInternalAPI.get_check`."""
        result = await self._get_check(
            GetRestrictionCheckCommand(check_id=input_data.check_id, current_user_id=input_data.current_user_id)
        )
        return self._to_result(result)

    @override
    async def delete_checks(self, input_data: DeleteChecksInput) -> None:
        """See :meth:`RestrictionInternalAPI.delete_checks`."""
        await self._delete_checks(
            DeleteRestrictionChecksCommand(check_ids=input_data.check_ids, current_user_id=input_data.current_user_id)
        )

    @staticmethod
    def _to_result(result: RestrictionCheckResponse) -> RestrictionCheckResult:
        """Map a use case response to the internal result, so no application DTO leaves the module."""
        return RestrictionCheckResult(
            id=result.id,
            parcel_id=result.parcel_id,
            rules_version=result.rules_version,
            created_at=result.created_at,
            hits=[
                RestrictionHitResult(
                    kind=hit.kind,
                    overlap_area_m2=hit.overlap_area_m2,
                    overlap_share=hit.overlap_share,
                    zone_names=list(hit.zone_names),
                    legal_basis=hit.legal_basis,
                )
                for hit in result.hits
            ],
        )


__all__ = ("RestrictionInternal",)
