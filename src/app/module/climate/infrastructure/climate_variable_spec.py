"""WorldClim 2.1 variable metadata (infrastructure concern).

Maps each domain :class:`ClimateVariable` to the external data-source details
needed to load and interpret its raster: the WorldClim BIO code, the S3 object
key of the COG, the physical unit, and the scale factor used to convert raw
stored values to that unit.

These details belong to the infrastructure layer because they describe how data
coming from outside the application is parsed, not the domain entity itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.module.climate.domain.value_object.raster.climate_variable import ClimateVariable


@dataclass(frozen=True, slots=True)
class ClimateVariableSpec:
    """External metadata for a single climate variable.

    Attributes
    ----------
    variable : ClimateVariable
        The domain variable this spec describes.
    code : str
        WorldClim variable code (e.g. ``BIO1``).
    object_key : str
        S3 object key of the regional COG in the climate bucket.
    scale : int
        Divisor applied to convert raw stored values to physical units
        (WorldClim stores temperature-derived variables scaled by 10 or 100).
    unit : str
        Physical unit of the converted value.
    """

    variable: ClimateVariable
    code: str
    object_key: str
    scale: int
    unit: str


#: Registry of external metadata for every supported climate variable.
CLIMATE_VARIABLE_SPECS: dict[ClimateVariable, ClimateVariableSpec] = {
    ClimateVariable.MEAN_ANNUAL_TEMPERATURE: ClimateVariableSpec(
        variable=ClimateVariable.MEAN_ANNUAL_TEMPERATURE,
        code="BIO1",
        object_key="bio_1.tif",
        scale=10,
        unit="°C",
    ),
    ClimateVariable.TEMPERATURE_SEASONALITY: ClimateVariableSpec(
        variable=ClimateVariable.TEMPERATURE_SEASONALITY,
        code="BIO4",
        object_key="bio_4.tif",
        scale=100,
        unit="°C",
    ),
    ClimateVariable.MAX_TEMPERATURE_WARMEST_MONTH: ClimateVariableSpec(
        variable=ClimateVariable.MAX_TEMPERATURE_WARMEST_MONTH,
        code="BIO5",
        object_key="bio_5.tif",
        scale=10,
        unit="°C",
    ),
    ClimateVariable.MIN_TEMPERATURE_COLDEST_MONTH: ClimateVariableSpec(
        variable=ClimateVariable.MIN_TEMPERATURE_COLDEST_MONTH,
        code="BIO6",
        object_key="bio_6.tif",
        scale=10,
        unit="°C",
    ),
    ClimateVariable.ANNUAL_PRECIPITATION: ClimateVariableSpec(
        variable=ClimateVariable.ANNUAL_PRECIPITATION,
        code="BIO12",
        object_key="bio_12.tif",
        scale=1,
        unit="mm",
    ),
    ClimateVariable.PRECIPITATION_WETTEST_MONTH: ClimateVariableSpec(
        variable=ClimateVariable.PRECIPITATION_WETTEST_MONTH,
        code="BIO13",
        object_key="bio_13.tif",
        scale=1,
        unit="mm",
    ),
    ClimateVariable.PRECIPITATION_DRIEST_MONTH: ClimateVariableSpec(
        variable=ClimateVariable.PRECIPITATION_DRIEST_MONTH,
        code="BIO14",
        object_key="bio_14.tif",
        scale=1,
        unit="mm",
    ),
    ClimateVariable.PRECIPITATION_SEASONALITY: ClimateVariableSpec(
        variable=ClimateVariable.PRECIPITATION_SEASONALITY,
        code="BIO15",
        object_key="bio_15.tif",
        scale=1,
        unit="%",
    ),
}


__all__ = (
    "CLIMATE_VARIABLE_SPECS",
    "ClimateVariableSpec",
)
