"""Shared entity-to-response mapping for restriction use cases."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.restriction.application.dto.response import RestrictionCheckResponse, RestrictionHitResponse


if TYPE_CHECKING:
    from app.module.restriction.domain.entity import RestrictionCheck


def to_check_response(check: RestrictionCheck) -> RestrictionCheckResponse:
    """Map a restriction check entity to its response DTO."""
    return RestrictionCheckResponse(
        id=check.id.unwrap(),
        parcel_id=check.parcel_id.unwrap(),
        rules_version=check.rules_version.unwrap(),
        created_at=check.created_at,
        hits=[
            RestrictionHitResponse(
                kind=hit.kind.value,
                overlap_area_m2=hit.overlap_area.unwrap(),
                overlap_share=hit.overlap_share.unwrap(),
                zone_names=list(hit.zone_names.unwrap()),
                legal_basis=hit.legal_basis.unwrap(),
            )
            for hit in check.hits
        ],
    )


__all__ = ("to_check_response",)
