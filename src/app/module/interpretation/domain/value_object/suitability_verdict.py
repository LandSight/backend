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
        """Human-readable Russian label."""
        return _LABELS[self]


_THRESHOLDS = (
    (0.8, SuitabilityVerdict.VERY_HIGH),
    (0.65, SuitabilityVerdict.HIGH),
    (0.5, SuitabilityVerdict.MEDIUM),
    (0.35, SuitabilityVerdict.LOW),
)

_LABELS = {
    SuitabilityVerdict.VERY_HIGH: "очень высокая пригодность",
    SuitabilityVerdict.HIGH: "высокая пригодность",
    SuitabilityVerdict.MEDIUM: "средняя пригодность",
    SuitabilityVerdict.LOW: "низкая пригодность",
    SuitabilityVerdict.VERY_LOW: "очень низкая пригодность",
}


__all__ = ("SuitabilityVerdict",)
