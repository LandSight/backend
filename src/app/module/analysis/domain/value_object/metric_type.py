"""Metric module type value object."""

from __future__ import annotations

from enum import StrEnum


class MetricType(StrEnum):
    """Module a referenced metrics snapshot belongs to."""

    TOPOGRAPHY = "topography"
    CLIMATE = "climate"
    INFRASTRUCTURE = "infrastructure"


__all__ = ("MetricType",)
