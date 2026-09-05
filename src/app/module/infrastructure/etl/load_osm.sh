#!/usr/bin/env bash
# Load OpenStreetMap data for the Leningrad region into the local PostGIS DB.
#
# Steps:
#   1. download the Geofabrik North-West federal district extract
#   2. cut out exactly the DEM bounding box with osmium
#   3. import into `infrastructure` schema with osm2pgsql (EPSG:3857)
#   4. verify counts
#
# Prerequisites: docker compose running Postgres, osmium, osm2pgsql, wget.
set -euo pipefail

DB_NAME="${DB_NAME:-landsight}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-15432}"
DB_USER="${DB_USER:-landsight}"
DB_PASS="${DB_PASS:-landsight}"

# DEM bounding box (west,south,east,north) — same as load_fabdem.py.
WEST=26.7
SOUTH=58.2
EAST=35.9
NORTH=61.5

# Geofabrik Northwestern Federal District (622 MB). The source lives under the
# `russia/` subdirectory — using a flat name would hit a 404 and wget would save
# an HTML error page that osmium rejects with "invalid BlobHeader".
PBF_URL="${PBF_URL:-https://download.geofabrik.de/russia/northwestern-fed-district-latest.osm.pbf}"
PBF_SRC="${PBF_SRC:-northwestern-fed-district-latest.osm.pbf}"
OUT_PBF="${OUT_PBF:-leningrad_bbox.osm.pbf}"

for cmd in wget osmium osm2pgsql docker; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "ERROR: required tool not found: $cmd" >&2
        exit 1
    fi
done

echo "==> Ensuring schema and extensions (idempotent)."
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 <<'SQL'
CREATE SCHEMA IF NOT EXISTS infrastructure AUTHORIZATION landsight;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;
SQL

if [ ! -f "$PBF_SRC" ]; then
    echo "==> Downloading $PBF_URL (~600 MB, may take a while)."
    wget -q -O "$PBF_SRC" "$PBF_URL"
fi

# Sanity check: a valid .pbf is binary and starts with null bytes, whereas a
# failed download yields an HTML error page (no null bytes in the first KB).
if ! head -c 1024 "$PBF_SRC" | grep -q $'\x00'; then
    echo "ERROR: $PBF_SRC does not look like a valid PBF (download failed or returned an error page)." >&2
    rm -f "$PBF_SRC"
    exit 1
fi

echo "==> Extracting bbox ${WEST},${SOUTH},${EAST},${NORTH} -> $OUT_PBF"
osmium extract -b "${WEST},${SOUTH},${EAST},${NORTH}" "$PBF_SRC" -o "$OUT_PBF"

# Drop leftovers from a previous run with the default osm2pgsql output (which
# creates planet_osm_line / planet_osm_roads without a `tags` column).
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 <<'SQL'
DROP TABLE IF EXISTS infrastructure.planet_osm_line;
DROP TABLE IF EXISTS infrastructure.planet_osm_roads;
DROP TABLE IF EXISTS infrastructure.osm2pgsql_properties;
SQL

LUA_STYLE="${LUA_STYLE:-$(dirname "$0")/osm2pgsql_flex.lua}"

echo "==> Importing into infrastructure.planet_osm_* (EPSG:3857, flex output)."
PGPASSWORD="$DB_PASS" osm2pgsql -c \
    -d "$DB_NAME" \
    -H "$DB_HOST" \
    -P "$DB_PORT" \
    -U "$DB_USER" \
    --output flex \
    --style "$LUA_STYLE" \
    --merc \
    "$OUT_PBF"

echo "==> Verification."
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c \
    "SELECT COUNT(*) AS schools FROM infrastructure.planet_osm_point WHERE tags->'amenity' = 'school';"
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c \
    "SELECT COUNT(*) AS bus_stops FROM infrastructure.planet_osm_point WHERE tags->'highway' = 'bus_stop';"

echo "==> Done."
