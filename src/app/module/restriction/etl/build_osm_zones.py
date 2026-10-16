"""Build the restriction zones from the imported OSM layers.

Reads the rules from ``zones.yaml`` and rebuilds ``restriction.zones`` in one
transaction, so a failed run leaves the previous zones in place. Run after
the OSM import (``load_osm.sh``) and after every change to the rules:

    uv run python -m app.module.restriction.etl.build_osm_zones
"""

from __future__ import annotations

import asyncio
import time

from sqlalchemy import text

from app.module.restriction.etl.rules import load_zone_rules
from app.module.restriction.etl.sql import build_insert
from app.platform.config.loaders import load_database_config
from app.platform.database.engine import create_async_engine_from_config, dispose_engine


async def build_zones() -> None:
    """Rebuild every restriction zone from the OSM layers."""
    rules = load_zone_rules()
    engine = create_async_engine_from_config(load_database_config())
    print(f"Building restriction zones, rules version {rules.version} ({len(rules.rules)} rules)")  # noqa: T201

    try:
        async with engine.begin() as connection:
            await connection.execute(text("DELETE FROM restriction.zones"))
            for rule in rules.rules:
                started = time.monotonic()
                sql, params = build_insert(rule, rules.version)
                result = await connection.execute(text(sql), params)
                print(  # noqa: T201
                    f"  {rule.id:<40} {rule.kind.value:<28} {result.rowcount:>7} zones"
                    f"  {time.monotonic() - started:6.1f} s"
                )
            await connection.execute(text("ANALYZE restriction.zones"))
    finally:
        await dispose_engine(engine)

    print("Done.")  # noqa: T201


def main() -> None:
    """Entry point."""
    asyncio.run(build_zones())


if __name__ == "__main__":
    main()
