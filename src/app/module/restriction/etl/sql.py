"""SQL generation for zone rules.

Each rule becomes one ``INSERT ... SELECT`` over an osm2pgsql layer. Values
from the rules file are passed as bound parameters; only ``extra_sql`` is
inlined, as trusted configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final

from app.module.restriction.etl.rules import DerivedAttribute, StepWidth, TagWidth


if TYPE_CHECKING:
    from app.module.restriction.etl.rules import ZoneRule


_LAYER_TABLES: Final = {
    "point": "infrastructure.planet_osm_point",
    "line": "infrastructure.planet_osm_line",
    "polygon": "infrastructure.planet_osm_polygon",
}

_AREA_M2: Final = "ST_Area(ST_Transform(way, 4326)::geography)"
_LENGTH_M: Final = "ST_Length(ST_Transform(way, 4326)::geography)"
# Pieces of one river are chained ways sharing a name; ways closer than this
# (in Web Mercator units) belong to the same river. Unnamed ways stand alone.
_RIVER_CLUSTER_EPS: Final = 100


@dataclass
class _Params:
    """Collects bound parameters under generated names."""

    values: dict[str, object] = field(default_factory=dict)

    def bind(self, value: str | float) -> str:
        """Bind a value and return its placeholder, typed so PostgreSQL never has to guess."""
        name = f"p{len(self.values)}"
        self.values[name] = value
        sql_type = "text" if isinstance(value, str) else "float8"
        return f"CAST(:{name} AS {sql_type})"


def build_insert(rule: ZoneRule, rules_version: str) -> tuple[str, dict[str, object]]:
    """Build the SQL that inserts the zones of one rule.

    Parameters
    ----------
    rule : ZoneRule
        The rule to build.
    rules_version : str
        Version recorded on every inserted zone.

    Returns
    -------
    tuple[str, dict[str, object]]
        SQL text and its bound parameters.
    """
    params = _Params()
    table = _LAYER_TABLES[rule.layer.value]
    ctes = _derived(rule, params)
    width = _width(rule, params)

    attributes = "'{}'::jsonb"
    if isinstance(rule.width, StepWidth):
        attributes = f"jsonb_build_object({params.bind(rule.width.by.value)}, round(attr::numeric, 3))"
    elif isinstance(rule.width, TagWidth):
        attributes = f"jsonb_build_object({params.bind(rule.width.tag)}, tags -> {params.bind(rule.width.tag)})"

    geometry = (
        "ST_Multi(ST_CollectionExtract(ST_MakeValid(CASE WHEN width_m > 0 "
        "THEN ST_Transform(ST_Buffer(ST_Transform(way, 4326)::geography, width_m)::geometry, 3857) "
        "ELSE way END), 3))"
    )

    # Identifiers come from the code and values are bound parameters; only the
    # trusted ``extra_sql`` of the rules file is inlined.
    sql = f"""
    WITH src AS (
        SELECT osm_id, coalesce(name, tags -> 'name') AS name, way, tags
        FROM {table}
        WHERE {_filter(rule, params)}
    ),
    {ctes}
    sized AS (
        SELECT osm_id, name, way, tags, attr, {width} AS width_m FROM derived
    ),
    built AS (
        SELECT osm_id, name, width_m, {attributes} AS attributes, {geometry} AS geom
        FROM sized
        WHERE width_m IS NOT NULL
    )
    INSERT INTO restriction.zones
        (id, kind, source_layer, source_osm_id, name, legal_basis, width_m, attributes, rules_version, geom)
    SELECT
        gen_random_uuid(), {params.bind(rule.kind.value)}, {params.bind(rule.layer.value)}, osm_id, name,
        {params.bind(rule.legal_basis)}, width_m, attributes, {params.bind(rules_version)}, geom
    FROM built
    WHERE NOT ST_IsEmpty(geom)
    """  # noqa: S608
    return sql, params.values


def _filter(rule: ZoneRule, params: _Params) -> str:
    """Build the tag filter of a rule."""
    alternatives = [
        "(" + " AND ".join(_tag_condition(key, values, params) for key, values in alternative.items()) + ")"
        for alternative in rule.match
    ]
    conditions = ["(" + " OR ".join(alternatives) + ")"]
    conditions.extend(
        f"NOT coalesce({_tag_condition(key, values, params)}, false)" for key, values in rule.exclude.items()
    )
    if rule.min_area_ha is not None:
        conditions.append(f"{_AREA_M2} >= {params.bind(rule.min_area_ha * 10_000)}")
    if rule.extra_sql:
        conditions.append(f"({rule.extra_sql})")
    return " AND ".join(conditions)


def _tag_condition(key: str, values: list[str], params: _Params) -> str:
    """Build the condition for one tag key and its accepted values."""
    if "*" in values:
        return f"tags ? {params.bind(key)}"
    placeholders = ", ".join(params.bind(value) for value in values)
    return f"tags -> {params.bind(key)} IN ({placeholders})"


def _derived(rule: ZoneRule, params: _Params) -> str:
    """Build the CTEs that compute the derived attribute, ending in ``derived`` with ``attr``."""
    if not isinstance(rule.width, StepWidth):
        return "derived AS (SELECT src.*, NULL::numeric AS attr FROM src),"

    match rule.width.by:
        case DerivedAttribute.AREA_HA:
            expression = f"{_AREA_M2} / 10000.0"
        case DerivedAttribute.VOLTAGE_KV:
            expression = _voltage_kv(rule.width, params)
        case DerivedAttribute.RIVER_LENGTH_KM:
            return (
                "clustered AS ("  # noqa: S608 - fixed SQL, no external values
                "SELECT src.*, coalesce(tags -> 'name', osm_id::text) AS grp, "
                f"ST_ClusterDBSCAN(way, eps := {_RIVER_CLUSTER_EPS}, minpoints := 1) "
                "OVER (PARTITION BY coalesce(tags -> 'name', osm_id::text)) AS cid FROM src"
                "),\n"
                "    derived AS ("
                "SELECT osm_id, name, way, tags, "
                f"sum({_LENGTH_M}) OVER (PARTITION BY grp, cid) / 1000.0 AS attr FROM clustered"
                "),"
            )
    return f"derived AS (SELECT src.*, ({expression})::numeric AS attr FROM src),"  # noqa: S608 - bound params only


def _voltage_kv(width: StepWidth, params: _Params) -> str:
    """Build the highest voltage of a power line in kV, with a default by line kind.

    OSM records volts, ``;``-separated for several circuits; values below
    1000 are taken to be kV already.
    """
    tagged = (
        "(SELECT CASE WHEN max(trim(v)::numeric) >= 1000 THEN max(trim(v)::numeric) / 1000 "
        "ELSE max(trim(v)::numeric) END "
        "FROM unnest(string_to_array(tags -> 'voltage', ';')) AS v "
        "WHERE trim(v) ~ '^[0-9]+(\\.[0-9]+)?$')"
    )
    if not width.default_kv:
        return tagged
    defaults = " ".join(f"WHEN {params.bind(kind)} THEN {params.bind(kv)}" for kind, kv in width.default_kv.items())
    return f"coalesce({tagged}, CASE tags -> 'power' {defaults} END)"


def _width(rule: ZoneRule, params: _Params) -> str:
    """Build the width expression of a rule, in meters."""
    if rule.width_m is not None:
        return params.bind(rule.width_m)
    if isinstance(rule.width, TagWidth):
        cases = " ".join(
            f"WHEN {params.bind(value)} THEN {params.bind(width)}" for value, width in rule.width.values.items()
        )
        default = "NULL" if rule.width.default is None else params.bind(rule.width.default)
        return f"CASE tags -> {params.bind(rule.width.tag)} {cases} ELSE {default} END"
    assert isinstance(rule.width, StepWidth)  # noqa: S101 - narrowed by the rule validator
    *steps, last = rule.width.steps
    # The validator guarantees every step but the last has a bound.
    bounded = [(step.max, step.width_m) for step in steps if step.max is not None]
    cases = " ".join(f"WHEN attr <= {params.bind(bound)} THEN {params.bind(width)}" for bound, width in bounded)
    return f"CASE {cases} ELSE {params.bind(last.width_m)} END" if cases else params.bind(last.width_m)


__all__ = ("build_insert",)
