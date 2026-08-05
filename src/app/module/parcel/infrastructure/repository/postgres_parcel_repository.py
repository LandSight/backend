"""PostgreSQL (PostGIS) parcel repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Polygon as ShapelyPolygon
from sqlalchemy import select

from app.module.parcel.application.port import ParcelRepository
from app.module.parcel.domain.entity import Parcel
from app.module.parcel.domain.value_object import (
    OwnerId,
    ParcelId,
    ParcelName,
)
from app.module.parcel.infrastructure.model import ParcelModel
from app.module.shared.domain.value_object import GeoPoint, Polygon
from app.platform.database.repository import BaseSQLAlchemyRepository


if TYPE_CHECKING:
    from geoalchemy2 import Geometry, WKBElement
    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresParcelRepository(BaseSQLAlchemyRepository, ParcelRepository):
    """Parcel repository backed by PostgreSQL with PostGIS extension.

    Stores polygon geometry in PostGIS ``Geometry(Polygon, 4326)`` column.
    Converts between domain :class:`~app.module.shared.domain.value_object.Polygon`
    and Shapely/PostGIS formats directly using coordinate data from the domain object.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    @override
    async def save(self, parcel: Parcel) -> None:
        """See :class:`app.module.parcel.application.port.ParcelRepository.save`."""
        shapely_geom = self._domain_to_shapely(parcel.polygon)
        wkb_element = from_shape(shapely_geom, srid=4326)

        model = ParcelModel(
            id=parcel.id.unwrap(),
            name=parcel.name.unwrap(),
            polygon=cast("Geometry", wkb_element),
            owner_id=parcel.owner_id.unwrap(),
        )
        self._session.add(model)

    @override
    async def get_by_id(self, parcel_id: ParcelId) -> Parcel | None:
        """See :class:`app.module.parcel.application.port.ParcelRepository.get_by_id`."""
        result = await self._session.execute(
            select(ParcelModel).where(ParcelModel.id == parcel_id.unwrap()),
        )
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model is not None else None

    @override
    async def get_by_owner_id(self, owner_id: OwnerId) -> list[Parcel]:
        """See :class:`app.module.parcel.application.port.ParcelRepository.get_by_owner_id`."""
        result = await self._session.execute(
            select(ParcelModel).where(ParcelModel.owner_id == owner_id.unwrap()),
        )
        models = result.scalars().all()

        return [self._to_domain(model) for model in models]

    @override
    async def delete(self, parcel_id: ParcelId) -> None:
        """See :class:`app.module.parcel.application.port.ParcelRepository.delete`."""
        result = await self._session.execute(
            select(ParcelModel).where(ParcelModel.id == parcel_id.unwrap()),
        )
        model = result.scalar_one_or_none()
        if model is not None:
            await self._session.delete(model)

    @staticmethod
    def _domain_to_shapely(polygon: Polygon) -> ShapelyPolygon:
        """Convert domain Polygon to Shapely Polygon for PostGIS storage.

        Shapely uses (x, y) = (lon, lat) order.
        """
        coords = [(point.longitude.unwrap(), point.latitude.unwrap()) for point in polygon.points]
        return ShapelyPolygon(coords)

    @staticmethod
    def _to_domain(model: ParcelModel) -> Parcel:
        """Convert an ORM model to a domain entity."""
        wkb_element = cast("WKBElement", model.polygon)
        shapely_geom = to_shape(wkb_element)

        points = [GeoPoint.create(float(coord[1]), float(coord[0])) for coord in shapely_geom.exterior.coords]
        domain_polygon = Polygon(tuple(points))

        return Parcel(
            id=ParcelId(model.id),
            name=ParcelName(model.name),
            polygon=domain_polygon,
            owner_id=OwnerId(model.owner_id),
        )


__all__ = ("PostgresParcelRepository",)
