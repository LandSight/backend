"""Restriction repositories."""

from __future__ import annotations

from .postgres_check_repository import PostgresCheckRepository
from .postgres_zone_repository import PostgresZoneRepository


__all__ = ("PostgresCheckRepository", "PostgresZoneRepository")
