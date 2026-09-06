#!/usr/bin/env bash
# Download WorldClim 2.1 bioclimatic variables, convert to regional COGs
# and upload to S3-compatible store (MinIO).
#
# Uses wget for reliable downloading with progress and gdal_translate for COG conversion.
# Bounding box: Leningrad oblast (26.7, 58.2, 35.9, 61.5)

set -euo pipefail

# Проверка зависимостей
for cmd in wget gdal_translate docker; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "ERROR: required tool not found: $cmd" >&2
        exit 1
    fi
done

# Переменные
BASE_URL="https://geodata.ucdavis.edu/climate/worldclim/2_1/base"
ZIP_FILE="wc2.1_30s_bio.zip"
VARIABLES=(1 4 5 6 12 13 14 15)
MIN_LON="26.7"
MAX_LAT="61.5"
MAX_LON="35.9"
MIN_LAT="58.2"
PROJWIN="$MIN_LON $MAX_LAT $MAX_LON $MIN_LAT"

# S3 настройки
S3_BUCKET="${S3_CLIMATE_BUCKET:-landsight-climate}"
S3_ACCESS_KEY="${S3_ACCESS_KEY:-admin}"
S3_SECRET_KEY="${S3_SECRET_KEY:-password123}"
MINIO_HOST="${MINIO_HOST:-minio}"
MINIO_PORT="${MINIO_PORT:-9000}"
COMPOSE_NETWORK="${COMPOSE_NETWORK:-}"

echo "==> Downloading WorldClim 2.1 variables for Leningrad region"

# 1) Скачиваем архив с прогресс-баром
if [ ! -f "$ZIP_FILE" ]; then
    echo "==> Downloading $ZIP_FILE (1.3 GB)..."
    wget -c --progress=bar:force "$BASE_URL/$ZIP_FILE"
    echo "==> Download complete"
else
    echo "==> $ZIP_FILE already exists, skipping download"
fi

# 2) Распаковываем только нужные файлы
echo "==> Extracting variables: ${VARIABLES[*]}"
for n in "${VARIABLES[@]}"; do
    FILENAME="wc2.1_30s_bio_${n}.tif"
    if [ ! -f "$FILENAME" ]; then
        unzip -j "$ZIP_FILE" "$FILENAME" -d .
        echo "  extracted $FILENAME"
    else
        echo "  $FILENAME already exists, skipping extraction"
    fi
done

# 3) Обрезаем до региона и конвертируем в COG
echo "==> Cropping to region and converting to COG"
for n in "${VARIABLES[@]}"; do
    SRC="wc2.1_30s_bio_${n}.tif"
    OUT="bio_${n}.tif"

    if [ -f "$OUT" ]; then
        echo "  $OUT already exists, skipping conversion"
        continue
    fi

    echo "  processing $SRC -> $OUT"

    # Исправленный вызов gdal_translate
    gdal_translate -q -of COG \
        -projwin $PROJWIN \
        -co COMPRESS=DEFLATE \
        -co BLOCKSIZE=256 \
        -co OVERVIEW_RESAMPLING=NEAREST \
        "$SRC" "$OUT"

    # Проверяем размер
    SIZE=$(du -h "$OUT" | cut -f1)
    echo "    -> $OUT ($SIZE)"
done

# 4) Загружаем в MinIO
echo "==> Uploading COGs to MinIO"

# Определяем сеть
if [ -z "${COMPOSE_NETWORK:-}" ]; then
    COMPOSE_NETWORK="$(docker network ls --format '{{.Name}}' | grep 'landsight-network$' | head -n1)"
fi
if [ -z "${COMPOSE_NETWORK:-}" ]; then
    echo "ERROR: compose network 'landsight-network' not found." >&2
    exit 1
fi

# Загружаем каждый файл
for n in "${VARIABLES[@]}"; do
    SRC="bio_${n}.tif"
    DST="bio_${n}.tif"
    echo "  uploading $SRC -> $S3_BUCKET/$DST"

    docker run --rm \
        --entrypoint sh \
        --network "$COMPOSE_NETWORK" \
        -v "$(pwd):/workdir" \
        minio/mc -c "
            mc alias set local http://$MINIO_HOST:$MINIO_PORT $S3_ACCESS_KEY $S3_SECRET_KEY >/dev/null && \
            mc mb --ignore-existing local/$S3_BUCKET >/dev/null && \
            mc cp /workdir/$SRC local/$S3_BUCKET/$DST
        "
done

echo "==> Done! All COGs uploaded to $S3_BUCKET"
echo "Files: bio_{1,4,5,6,12,13,14,15}.tif"
