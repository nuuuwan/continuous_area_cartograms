import topojson
from shapely import MultiPolygon as ShapelyMultiPolygon
from shapely import Polygon as ShapelyPolygon
from utils import JSONFile, Log

log = Log('DNCLoader')


class DNCLoader:
    # loaders
    @staticmethod
    def extract_shapely_polygon(geometry):
        if isinstance(geometry, ShapelyPolygon):
            return geometry

        if isinstance(geometry, ShapelyMultiPolygon):
            return max(
                geometry.geoms,
                key=lambda polygon: polygon.area,
            )

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @classmethod
    def from_topojson(cls, topojson_path, get_ids, id_to_value=None):
        if id_to_value is None:
            id_to_value = {}
        data = JSONFile(topojson_path).read()
        objects = data['objects']
        objects_name = list(objects.keys())[0]
        geometries = objects[objects_name]['geometries']
        n_geometries = len(geometries)
        log.debug(f'Read {n_geometries} {objects_name} from {topojson_path}')
        topo = topojson.Topology(data, object_name=objects_name)
        gdf = topo.to_gdf()
        geometries = gdf['geometry']
        id_nums = get_ids(gdf)

        id_to_shapely_polygons = {}
        for geometry, id_num in zip(geometries, id_nums):
            id = 'LK-' + str(id_num)
            shapely_polygon = cls.extract_shapely_polygon(geometry)
            id_to_shapely_polygons[id] = shapely_polygon

        return cls(id_to_shapely_polygons, id_to_value)

    @classmethod
    def from_ents(cls, ents, id_to_value):
        id_to_shapely_polygons = {}
        for ent in ents:
            gdf = ent.geo()

            shapely_polygon = cls.extract_shapely_polygon(gdf['geometry'][0])
            id_to_shapely_polygons[ent.id] = shapely_polygon
        return cls(id_to_shapely_polygons, id_to_value)
