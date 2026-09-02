"""Download FabDEM elevation data for the Leningrad region.

Downloads a Cloud Optimized GeoTIFF covering the requested bounding box
into ``leningrad_oblast_dem.tif``.
"""

from __future__ import annotations

import fabdem


def main() -> None:
    """Download the DEM for the Leningrad region."""
    bounds = (26.7, 58.2, 35.9, 61.5)
    fabdem.download(bounds, output_path="leningrad_oblast_dem.tif")


if __name__ == "__main__":
    main()
