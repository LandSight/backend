"""Add postgis extension.

Revision ID: ef70c85c6229
Revises: fd780af9c921
Create Date: 2026-07-15 11:21:42.429355

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "ef70c85c6229"
down_revision: str | Sequence[str] | None = "fd780af9c921"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable PostGIS extension (required for Geometry type used by Parcel module).
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS postgis")
