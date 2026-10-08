"""Suitability verdict value object."""

from __future__ import annotations

from enum import StrEnum


class SuitabilityVerdict(StrEnum):
    """Qualitative verdict of a parcel's suitability derived from its score.

    The verdict is decided by fixed thresholds on the share of the maximum
    score, never by the model.
    """

    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

    @classmethod
    def from_ratio(cls, ratio: float) -> SuitabilityVerdict:
        """Return the verdict for a score expressed as a share of the maximum."""
        for threshold, verdict in _THRESHOLDS:
            if ratio >= threshold:
                return verdict
        return cls.VERY_LOW

    @property
    def label(self) -> str:
        """Human-readable label."""
        return _LABELS[self]


_THRESHOLDS = (
    (0.8, SuitabilityVerdict.VERY_HIGH),
    (0.65, SuitabilityVerdict.HIGH),
    (0.5, SuitabilityVerdict.MEDIUM),
    (0.35, SuitabilityVerdict.LOW),
)

_LABELS = {
    SuitabilityVerdict.VERY_HIGH: "very high suitability",
    SuitabilityVerdict.HIGH: "high suitability",
    SuitabilityVerdict.MEDIUM: "medium suitability",
    SuitabilityVerdict.LOW: "low suitability",
    SuitabilityVerdict.VERY_LOW: "very low suitability",
}


__all__ = ("SuitabilityVerdict",)
