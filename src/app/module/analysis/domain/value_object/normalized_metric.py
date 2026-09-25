"""Normalized metric value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.domain.value_object.analysis_key import AnalysisKey
    from app.module.analysis.domain.value_object.normalized_score import NormalizedScore


@dataclass(frozen=True, slots=True)
class NormalizedMetric(BaseCompositeValueObject):
    """A raw metric reading and the result of normalizing it.

    Attributes
    ----------
    key : AnalysisKey
        Canonical metric key.
    raw_value : float | None
        Raw reading; ``None`` when the metric is unavailable.
    normalized_value : NormalizedScore | None
        Normalized value in ``[0, 1]``; ``None`` when unavailable.
    unit : str
        Unit of the raw value.
    function_name : str | None
        Name of the normalization function applied, for provenance.
    function_params : Mapping[str, float] | None
        Parameters of the normalization function applied.
    """

    key: AnalysisKey
    raw_value: float | None
    normalized_value: NormalizedScore | None
    unit: str = ""
    function_name: str | None = None
    function_params: Mapping[str, float] | None = None

    def _validate(self) -> None:
        if self.normalized_value is not None and self.raw_value is None:
            message = f"Metric '{self.key.unwrap()}' has a normalized value without a raw reading."
            raise ValidationError(message)

    @property
    def data_available(self) -> bool:
        """Whether a usable normalized reading is available."""
        return self.normalized_value is not None


__all__ = ("NormalizedMetric",)
