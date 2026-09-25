"""Analysis type (evaluation profile) value object."""

from __future__ import annotations

from enum import StrEnum


class AnalysisType(StrEnum):
    """Evaluation profile an analysis is run with.

    A profile selects the hierarchy and fuzzy-function configuration used to
    score a parcel. Only the individual housing construction profile is
    available today; new profiles (for example agriculture or commercial use)
    are added here together with their matching configurations.

    ``IZHS``
        Individual housing construction suitability.
    """

    IZHS = "izhs"


__all__ = ("AnalysisType",)
