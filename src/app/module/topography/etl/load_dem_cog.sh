#!/usr/bin/env bash
# Download the Leningrad region DEM, convert it to a Cloud Optimized GeoTIFF
# (COG) and upload it to the S3-compatible store (MinIO).
#
# The object is written under exactly the key the topography module reads:
#     <dem_bucket>/leningrad_oblast_dem_cog.tif
# (see s3_local_dem_repository._DEM_KEY).
#
# The bounding box is the same as `load_fabdem.py` and the OSM import.
#
# Prerequisites: `uv`, `docker` (MinIO + minio/mc image running via compose)
# and `gdal_translate` (GDAL >= 3.1).
set -euo pipefail

for cmd in uv gdal_translate docker; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "ERROR: required tool not found: $cmd" >&2
        exit 1
    fi
done

SRC_TIF="${SRC_TIF:-leningrad_oblast_dem.tif}"
COG_TIF="${COG_TIF:-leningrad_oblast_dem_cog.tif}"

# S3 / MinIO settings (defaults match .env.example and docker-compose.yml).
S3_BUCKET="${S3_DEM_BUCKET:-landsight-dem}"
S3_ACCESS_KEY="${S3_ACCESS_KEY:-admin}"
S3_SECRET_KEY="${S3_SECRET_KEY:-password123}"
# Resolved automatically below (compose prefixes it with the project name);
# can be overridden explicitly via the COMPOSE_NETWORK env var.
COMPOSE_NETWORK="${COMPOSE_NETWORK:-}"
MINIO_HOST="${MINIO_HOST:-minio}"   # service name on the compose network
MINIO_PORT="${MINIO_PORT:-9000}"

# 1) Download the DEM (same bounds as load_fabdem.py: 26.7,58.2,35.9,61.5).
echo "==> Downloading Leningrad DEM -> $SRC_TIF"
# uv run python src/app/module/topography/etl/load_fabdem.py
if [ ! -f "$SRC_TIF" ]; then
    echo "ERROR: DEM not downloaded: $SRC_TIF" >&2
    exit 1
fi

# 2) Convert to a Cloud Optimized GeoTIFF.
echo "==> Converting to COG -> $COG_TIF"
gdal_translate -q -of COG \
    -co COMPRESS=DEFLATE \
    -co BLOCKSIZE=256 \
    -co OVERVIEW_RESAMPLING=AVERAGE \
    "$SRC_TIF" "$COG_TIF"

if [ ! -f "$COG_TIF" ]; then
    echo "ERROR: COG conversion failed: $COG_TIF" >&2
    exit 1
fi

# 3) Upload to MinIO using the minio/mc image on the compose network.
#    NOTE: the minio/mc image has ENTRYPOINT ["mc"], so we override it with
#    `--entrypoint sh` to be able to run the multi-command shell snippet.
# Make sure MinIO is up (creates the compose network too).
docker compose up --detach --wait minio >/dev/null

# Compose prefixes networks with the project name (e.g. backend_landsight-network),
# so resolve the real name instead of hardcoding it.
if [ -z "${COMPOSE_NETWORK:-}" ]; then
    COMPOSE_NETWORK="$(docker network ls --format '{{.Name}}' | grep 'landsight-network$' | head -n1)"
fi
if [ -z "${COMPOSE_NETWORK:-}" ]; then
    echo "ERROR: compose network 'landsight-network' not found." >&2
    exit 1
fi

echo "==> Uploading $COG_TIF -> $S3_BUCKET/$COG_TIF"
docker run --rm \
    --entrypoint sh \
    --network "$COMPOSE_NETWORK" \
    -v "$(pwd):/workdir" \
    minio/mc -c "
        mc alias set local http://$MINIO_HOST:$MINIO_PORT $S3_ACCESS_KEY $S3_SECRET_KEY >/dev/null && \
        mc mb --ignore-existing local/$S3_BUCKET >/dev/null && \
        mc cp /workdir/$COG_TIF local/$S3_BUCKET/$COG_TIF
    "

echo "==> Done. Object: $S3_BUCKET/$COG_TIF"
