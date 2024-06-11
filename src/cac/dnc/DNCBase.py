from functools import cached_property

from geopandas import GeoDataFrame
from shapely import MultiPolygon as ShapelyMultiPolygon
from shapely import Polygon as ShapelyPolygon
from utils import Log

from cac.core import GroupedPolygon, GroupedPolygonGroup, Polygon, PolygonGroup

log = Log('DNCBase')


class DNCBase:
    def __init__(self, gdf: GeoDataFrame, values: list[float]):
        self.gdf = gdf
        self.values = values

    @staticmethod
    def extract_shapely_polygon_base(geometry):
        if isinstance(geometry, ShapelyPolygon):
            return geometry

        if isinstance(geometry, ShapelyMultiPolygon):
            return max(
                geometry.geoms,
                key=lambda polygon: polygon.area,
            )

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @staticmethod
    def extract_shapely_polygon(geometry, tolerance=0.001):
        shapely_polygon = DNCBase.extract_shapely_polygon_base(geometry)
        # The simplify method uses the Douglas-Peucker algorithm, which works
        # by iteratively removing points from the shape's boundary until all
        # remaining points are at least tolerance distance away from the
        # original boundary.
        if tolerance > 0:
            shapely_polygon = shapely_polygon.simplify(tolerance)
        return shapely_polygon

    # serializers
    def save_gdf(self, gdf_path):
        self.gdf.to_file(gdf_path, driver='GeoJSON')
        log.info(f'Wrote gdf to {gdf_path}')

    # shapely
    @cached_property
    def shapely_polygons(self):
        return [
            DNCBase.extract_shapely_polygon(geo)
            for geo in self.gdf['geometry']
        ]

    @cached_property
    def values(self):
        return [self.values[i] for i in range(len(self.gdf))]

    # core shapes
    @cached_property
    def polygons(self):
        polygons = []
        for shapely_polygon, value in zip(self.shapely_polygons, self.values):
            polygon = Polygon(id, shapely_polygon, value)
            polygons.append(polygon)

        return polygons

    @cached_property
    def polygon_group(self):
        return PolygonGroup(self.polygons)

    @cached_property
    def grouped_polygons(self):
        polygon_group = self.polygon_group
        return [
            GroupedPolygon(polygon, polygon_group)
            for polygon in self.polygons
        ]

    @cached_property
    def grouped_polygon_group(self):
        return GroupedPolygonGroup(self.grouped_polygons)
