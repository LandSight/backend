"""Fuzzy metric normalizer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.analysis.domain.value_object import AnalysisKey, NormalizedMetric, NormalizedScore
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.infrastructure.ports import FuzzyFunction


class FuzzyNormalizer:
    """Normalizes metrics with configured fuzzy membership functions."""

    def __init__(self, functions: Mapping[str, FuzzyFunction]) -> None:
        self._functions: dict[str, FuzzyFunction] = dict(functions)

    def normalize(self, key: str, value: float | None) -> NormalizedMetric:
        """Normalize one metric reading.

        Parameters
        ----------
        key : str
            Canonical metric key.
        value : float | None
            Raw reading; ``None`` when the metric is unavailable.

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
            return NormalizedMetric(
                key=analysis_key,
                raw_value=None,
                normalized_value=None,
                unit=function.unit,
                function_name=function.name,
                function_params=function.params(),
            )
        raw_value = float(value)
        return NormalizedMetric(
            key=analysis_key,
            raw_value=raw_value,
            normalized_value=NormalizedScore(function(raw_value)),
            unit=function.unit,
            function_name=function.name,
            function_params=function.params(),
        )


__all__ = ("FuzzyNormalizer",)
