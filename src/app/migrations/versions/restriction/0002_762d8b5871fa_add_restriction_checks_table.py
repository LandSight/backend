"""Add restriction checks table.

A check is an append-only snapshot of the zones overlapping a parcel.

Revision ID: 762d8b5871fa
Revises: d23e62e90475
Create Date: 2026-10-16 10:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "762d8b5871fa"
down_revision: str | Sequence[str] | None = "d23e62e90475"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "checks",
        sa.Column("parcel_id", sa.UUID(), nullable=False, comment="ID of the checked parcel"),
        sa.Column(
            "rules_version",
            sa.String(length=64),
            nullable=False,
            comment="Version of the zone rules the zones were built with",
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parcel_id"], ["parcel.parcels.id"], name=op.f("fk_checks_parcel_id_parcels"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_checks")),
        schema="restriction",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("checks", schema="restriction")
