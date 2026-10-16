"""Analysis status reason value object."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object.metric_type import MetricType


class AnalysisStatusReason(BaseValueObject[str]):
    """Value object for a human-readable analysis status explanation.

    The reason is shown to the user as is, so it must never carry raw error
    text (hosts, buckets, SQL, stack details): pipeline failures use the
    stage-specific factories below, and the error itself goes to the logs.

    Rules:
    - Must not be empty
    - Normalized: stripped and truncated to 512 characters (the column size)
    """

    _MAX_LENGTH = 512

    @classmethod
    def metrics_collection_failed(cls, metric_type: MetricType) -> AnalysisStatusReason:
        """Reason for a failure while collecting one metrics module."""
        return cls(f"Failed to collect {metric_type.value} data for the parcel. Please try again later.")

    @classmethod
    def restrictions_check_failed(cls) -> AnalysisStatusReason:
        """Reason for a failure while checking the restrictions on the parcel."""
        return cls("Failed to check the land-use restrictions of the parcel. Please try again later.")

    @classmethod
    def scoring_failed(cls) -> AnalysisStatusReason:
        """Reason for a failure while scoring the analysis."""
        return cls("Failed to calculate the analysis score. Please try again later.")

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()[: self._MAX_LENGTH]

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Analysis status reason must not be empty."
            raise ValidationError(message)


__all__ = ("AnalysisStatusReason",)
