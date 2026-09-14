-- osm2pgsql flex style for the Infrastructure module.
--
-- Creates `planet_osm_point` and `planet_osm_polygon` with exactly the columns
-- the application ORM models expect: osm_id, name, way, tags (hstore).
--
-- The default osm2pgsql "pgsql" output (as of 1.11) no longer emits a generic
-- `tags` hstore column, so we define it explicitly here.

local tables = {}

tables.point = osm2pgsql.define_table({
    name = 'planet_osm_point',
    schema = 'infrastructure',
    ids = { type = 'node', id_column = 'osm_id' },
    columns = {
        { column = 'name', type = 'text' },
        { column = 'way', type = 'point' },
        { column = 'tags', type = 'hstore' },
    },
    indexes = { { column = 'way', method = 'gist' } },
})

tables.polygon = osm2pgsql.define_table({
    name = 'planet_osm_polygon',
    schema = 'infrastructure',
    ids = { type = 'area', id_column = 'osm_id' },
    columns = {
        { column = 'name', type = 'text' },
        { column = 'way', type = 'geometry' },
        { column = 'tags', type = 'hstore' },
    },
    indexes = { { column = 'way', method = 'gist' } },
})

-- Only store nodes that carry tags (all infrastructure features are tagged).
function osm2pgsql.process_node(object)
    if object.tags and next(object.tags) then
        tables.point:insert({
            name = object.tags.name,
            way = object:as_point(),
            tags = object.tags,
        })
    end
end

function osm2pgsql.process_way(object)
    if object.is_closed and object.tags and next(object.tags) then
        local polygon = object:as_polygon()
        if polygon then
            tables.polygon:insert({
                name = object.tags.name,
                way = polygon,
                tags = object.tags,
            })
        end
    end
end

function osm2pgsql.process_relation(object)
    local area = object:as_multipolygon()
    if area and object.tags and next(object.tags) then
        tables.polygon:insert({
            name = object.tags.name,
            way = area,
            tags = object.tags,
        })
    end
end
