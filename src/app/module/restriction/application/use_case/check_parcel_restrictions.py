"""Check parcel restrictions use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, override
from uuid import uuid6

from app.module.restriction.application.dto.command import CheckParcelRestrictionsCommand
from app.module.restriction.application.dto.response import RestrictionCheckResponse
from app.module.restriction.application.error import RestrictionZonesNotLoadedError
from app.module.restriction.application.use_case._mapping import to_check_response
from app.module.restriction.domain.entity import RestrictionCheck
from app.module.restriction.domain.policy import POSITIONAL_TOLERANCE_M
from app.module.restriction.domain.value_object import ParcelId, RestrictionCheckId
from app.module.shared.application.use_case import BaseUseCase
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from app.module.restriction.application.port import CheckRepository, ParcelProvider, ZoneRepository


class CheckParcelRestrictionsUseCase(BaseUseCase[CheckParcelRestrictionsCommand, RestrictionCheckResponse]):
    """Find the restriction zones that overlap a parcel and store the result.

    Fetches the authoritative parcel geometry from the Parcel module (which
    enforces access), intersects it with the prebuilt zones and persists the
    result as an append-only snapshot, so analyses keep referencing the exact
    check they were scored with.
    """

    def __init__(
        self,
        zone_repository: ZoneRepository,
        check_repository: CheckRepository,
        parcel_provider: ParcelProvider,
    ) -> None:
        self._zone_repository = zone_repository
        self._check_repository = check_repository
        self._parcel_provider = parcel_provider
        self._logger = get_logger("app.restriction.use_case.check_parcel_restrictions")

    @override
    async def __call__(self, command: CheckParcelRestrictionsCommand) -> RestrictionCheckResponse:
        self._logger.info("Checking parcel restrictions: parcel_id=%s", command.parcel_id)

        # The Parcel module returns the geometry only for authorized users,
        # so this doubles as the access control gate for the check.
        polygon = await self._parcel_provider.get_parcel_polygon(command.parcel_id, command.current_user_id)

        rules_version = await self._zone_repository.rules_version()
        if rules_version is None:
            self._logger.warning("No restriction zones loaded: parcel_id=%s", command.parcel_id)
            raise RestrictionZonesNotLoadedError

        hits = await self._zone_repository.find_overlaps(polygon, POSITIONAL_TOLERANCE_M)
        check = RestrictionCheck(
            id=RestrictionCheckId(uuid6()),
            parcel_id=ParcelId(command.parcel_id),
            hits=tuple(sorted(hits, key=lambda hit: hit.kind.value)),
            rules_version=rules_version,
        )
        persisted = await self._check_repository.save(check)

        self._logger.info(
            "Parcel restrictions checked: id=%s parcel_id=%s kinds=%s",
            persisted.id,
            command.parcel_id,
            [hit.kind.value for hit in persisted.hits],
        )
        return to_check_response(persisted)


__all__ = ("CheckParcelRestrictionsUseCase",)
