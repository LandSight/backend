from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from app.platform.config.loaders import load_app_config
from app.platform.database.engine import create_async_engine_from_config, dispose_engine
from app.platform.logging import configure_logging


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from litestar import Litestar


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None]:
    """Application lifespan: create engine on startup, dispose on shutdown."""
    config = load_app_config()
    configure_logging(config.logging)

    engine = create_async_engine_from_config(config.database)
    app.state.engine = engine

    try:
        yield
    finally:
        await dispose_engine(engine)


__all__ = ("lifespan",)
