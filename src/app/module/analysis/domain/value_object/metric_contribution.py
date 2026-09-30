"""Metric contribution value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.domain.value_object.analysis_key import AnalysisKey
    from app.module.analysis.domain.value_object.contribution import Contribution
    from app.module.analysis.domain.value_object.normalized_score import NormalizedScore
    from app.module.analysis.domain.value_object.weight import Weight


@dataclass(frozen=True, slots=True)
class MetricContribution(BaseCompositeValueObject):
    """One metric's input to its parent aggregation node.

    Attributes
    ----------
    key : AnalysisKey
        Metric key.
    raw_value : float | None
        Raw reading; ``None`` when unavailable.
    normalized_value : NormalizedScore | None
        Normalized value in ``[0, 1]``; ``None`` when unavailable.
    weight : Weight
        Configured weight among siblings.
    contribution : Contribution | None
        ``normalized_value * weight``; ``None`` when unavailable.
    unit : str
        Unit of the raw value.
    membership_function : str | None
        Name of the normalization function applied.
    membership_params : Mapping[str, float] | None
        Parameters of the normalization function applied.
    """

    key: AnalysisKey
    raw_value: float | None
    normalized_value: NormalizedScore | None
    weight: Weight
    contribution: Contribution | None
    unit: str
    membership_function: str | None = None
    membership_params: Mapping[str, float] | None = None

    def _validate(self) -> None:
        if (self.normalized_value is None) != (self.contribution is None):
            message = f"Metric '{self.key.unwrap()}' must have both a normalized value and a contribution, or neither."
            raise ValidationError(message)
        if self.contribution is not None and self.contribution.unwrap() > self.weight.unwrap() + 1e-9:
            message = (
                f"Metric '{self.key.unwrap()}' contribution {self.contribution.unwrap()} "
                f"exceeds its weight {self.weight.unwrap()}."
            )
            raise ValidationError(message)

    @property
    def data_available(self) -> bool:
        """Whether a usable reading was available."""
        return self.normalized_value is not None


__all__ = ("MetricContribution",)
