# Changelog

<!-- towncrier release notes start -->

## [1.0.0](https://github.com/LandSight/backend/releases/tag/1.0.0) - 2026-09-14

### Feature

- Add parcel analysis: start an analysis, follow its status and stage, read the resulting score, and delete analyses.
- Add climate metrics for a parcel from WorldClim bioclimatic data.
- Add infrastructure metrics for a parcel by category (schools, hospitals, shops, transit stops, water bodies), including object count, minimum distance, and buffer coverage.
- Add topography metrics for a parcel from a digital elevation model: elevation, slope, aspect, area, perimeter, and shape indices.
- Add parcel management: create, list, view, and delete parcels with polygon geometry, and check parcel ownership.
- Add user accounts with JWT authentication: registration, login, token refresh, and profile retrieval.
- Add meta data about the API version.
- Add system healthcheck endpoint.
- Add asgi application.

### Ops

- Add a Docker Compose stack with PostgreSQL/PostGIS, Redis, and MinIO, including services for migrations, the API, and the background worker.
- Add a background worker for analysis with configurable concurrency.
- Add data preparation for elevation, climate, and OpenStreetMap layers.
- Add environment configuration for authentication, database, Redis, and object storage.
- Add per-module database migrations managed by Alembic.
- Migrate from mkdocs to zensical.
