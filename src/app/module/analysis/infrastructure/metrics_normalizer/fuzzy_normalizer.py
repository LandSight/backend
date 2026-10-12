"""Fuzzy metric normalizer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.analysis.domain.value_object import AnalysisKey, NormalizedMetric, NormalizedScore
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.infrastructure.metrics_normalizer import FuzzyFunction


class FuzzyNormalizer:
    """Normalizes metrics with configured fuzzy membership functions.

    A metric listed in ``missing_values`` that has no reading is normalized as
    if it read that value instead of being left unavailable. It is meant for
    metrics where finding nothing within the search buffer is itself a
    result, e.g. no power line within 1 km reads as 1 km away.
    """

    def __init__(
        self,
        functions: Mapping[str, FuzzyFunction],
        missing_values: Mapping[str, float] | None = None,
    ) -> None:
        self._functions: dict[str, FuzzyFunction] = dict(functions)
        self._missing_values: dict[str, float] = dict(missing_values or {})

    def normalize(self, key: str, value: float | None, label: str = "") -> NormalizedMetric:
        """Normalize one metric reading.

        Parameters
        ----------
        key : str
            Canonical metric key.
        value : float | None
            Raw reading; ``None`` when the metric is unavailable, in which case
            the configured missing value of the metric is used, if any.
        label : str
            Human-readable metric name; empty when not available.

        Returns
        -------
        NormalizedMetric
            The reading with its normalized value and provenance.

        Raises
        ------
        ValidationError
            If no fuzzy function is configured for ``key``.
        """
        function = self._functions.get(key)
        if function is None:
            message = f"No fuzzy function configured for metric '{key}'."
            raise ValidationError(message)
        analysis_key = AnalysisKey(key)
        if value is None:
            value = self._missing_values.get(key)
        if value is None:
            return NormalizedMetric(
                key=analysis_key,
                raw_value=None,
                normalized_value=None,
                unit=function.unit,
                label=label,
                function_name=function.name,
                function_params=function.params(),
            )
        raw_value = float(value)
        return NormalizedMetric(
            key=analysis_key,
            raw_value=raw_value,
            normalized_value=NormalizedScore(function(raw_value)),
            unit=function.unit,
            label=label,
            function_name=function.name,
            function_params=function.params(),
        )


__all__ = ("FuzzyNormalizer",)
