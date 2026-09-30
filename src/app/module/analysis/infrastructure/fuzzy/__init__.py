"""Fuzzy normalization infrastructure."""

from __future__ import annotations

from .fuzzy_normalizer import FuzzyNormalizer
from .s_shaped import SShaped
from .trapezoidal import Trapezoidal
from .z_shaped import ZShaped


__all__ = (
    "FuzzyNormalizer",
    "SShaped",
    "Trapezoidal",
    "ZShaped",
)
