"""SQLAlchemy model for the transactional outbox."""

from __future__ import annotations

import datetime  # noqa: TC003

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class OutboxEventModel(TimestampedModel):
    """ORM model for an outbox event.

    Maps to the ``outbox_events`` table in the default (public) schema. An event
    is written in the same transaction as the state change that produced it, so
    it is published at most once and never lost even if the process crashes
    before dispatching it.
    """

    __tablename__ = "outbox_events"

    event_type: Mapped[str] = mapped_column(
        sa.String(128),
        nullable=False,
        index=True,
        comment="Dotted event type (e.g. analysis.analysis_deleted)",
    )
    payload: Mapped[dict[str, object]] = mapped_column(
        JSONB,
        nullable=False,
        comment="Self-contained event payload",
    )
    published_at: Mapped[datetime.datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
        index=True,
        default=None,
        comment="When the event was dispatched; NULL while pending",
    )
    attempts: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=0,
        server_default=sa.text("0"),
        comment="Number of failed dispatch attempts",
    )
    last_error: Mapped[str | None] = mapped_column(
        sa.String(1024),
        nullable=True,
        default=None,
        comment="Last dispatch error; NULL when never failed",
    )


__all__ = ("OutboxEventModel",)
