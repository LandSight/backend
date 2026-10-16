"""Add interpretation generation attempt and progress.

The running report is owned by one generation attempt: the worker writes its
progress and the result only while the report still carries its attempt, so a
cancelled, regenerated or deleted report is never overwritten. The progress is
counted in generated texts and shown to the user while the report is running.

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2026-10-16 12:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "d5e6f7a8b9c0"
down_revision: str | Sequence[str] | None = "c4d5e6f7a8b9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "interpretations",
        sa.Column(
            "attempt_id",
            sa.UUID(),
            nullable=True,
            comment="Generation attempt that owns the running report",
        ),
        schema="interpretation",
    )
    op.add_column(
        "interpretations",
        sa.Column(
            "progress_done",
            sa.Integer(),
            server_default="0",
            nullable=False,
            comment="Texts generated so far by the running attempt",
        ),
        schema="interpretation",
    )
    op.add_column(
        "interpretations",
        sa.Column(
            "progress_total",
            sa.Integer(),
            server_default="0",
            nullable=False,
            comment="Texts the running attempt has to generate",
        ),
        schema="interpretation",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("interpretations", "progress_total", schema="interpretation")
    op.drop_column("interpretations", "progress_done", schema="interpretation")
    op.drop_column("interpretations", "attempt_id", schema="interpretation")


__all__ = ("down_revision", "downgrade", "revision", "upgrade")
