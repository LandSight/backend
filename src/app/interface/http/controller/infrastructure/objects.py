"""Infrastructure object HTTP endpoints.

Returns the objects a metrics snapshot was computed over as a GeoJSON
FeatureCollection, so the UI can show exactly the spatial scope behind a metric.
"""

from __future__ import annotations

from uuid import UUID

from litestar import get
from litestar.controller import Controller
from litestar.status_codes import HTTP_200_OK

from app.interface.http.schema.current_user import CurrentUser
from app.interface.http.schema.geojson import (
    GeoJSONLineString,
    GeoJSONPoint,
    GeoJSONPolygon,
)
from app.interface.http.schema.infrastructure import (
    InfrastructureObjectFeatureCollectionSchema,
    InfrastructureObjectFeatureSchema,
    InfrastructureObjectPropertiesSchema,
)
from app.interface.http.util.guards import require_authorization
from app.module.infrastructure.interface.internal.dto import GetObjectsInput
from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI
from app.module.shared.interface.internal.geojson import (
    GeoJSONLineString as InternalGeoJSONLineString,
    GeoJSONPoint as InternalGeoJSONPoint,
    GeoJSONPolygon as InternalGeoJSONPolygon,
)


class InfrastructureObjectsController(Controller):
    """Infrastructure object endpoints."""

    path = "/objects"
    tags = ("infrastructure",)
    guards = [require_authorization]

    @get(
        "/",
        status_code=HTTP_200_OK,
        description="List the objects a metrics snapshot was computed over.",
    )
    async def get_objects(
        self,
        category: str,
        metrics_id: UUID,
        infrastructure_api: InfrastructureInternalAPI,
        current_user: CurrentUser,
    ) -> InfrastructureObjectFeatureCollectionSchema:
        """List the objects a metrics snapshot was computed over."""
        result = await infrastructure_api.get_objects(
            GetObjectsInput(
                category=category,
                metrics_id=metrics_id,
                current_user_id=current_user.id,
            )
        )
        return InfrastructureObjectFeatureCollectionSchema(
            features=[
                InfrastructureObjectFeatureSchema(
                    geometry=self._to_geometry_schema(feature.geometry),
                    properties=InfrastructureObjectPropertiesSchema(
                        osm_id=feature.properties.osm_id,
                        name=feature.properties.name,
                        category=feature.properties.category,
                    ),
                )
                for feature in result.features
            ],
        )

    @staticmethod
    def _to_geometry_schema(
        geometry: InternalGeoJSONPoint | InternalGeoJSONLineString | InternalGeoJSONPolygon,
    ) -> GeoJSONPoint | GeoJSONLineString | GeoJSONPolygon:
        """Map an internal GeoJSON geometry to the HTTP schema."""
        if isinstance(geometry, InternalGeoJSONPoint):
            return GeoJSONPoint(coordinates=geometry.coordinates)
        if isinstance(geometry, InternalGeoJSONLineString):
            return GeoJSONLineString(coordinates=geometry.coordinates)
        return GeoJSONPolygon(coordinates=geometry.coordinates)


__all__ = ("InfrastructureObjectsController",)
