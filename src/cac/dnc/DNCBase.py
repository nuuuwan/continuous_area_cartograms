from functools import cached_property

from geopandas import GeoDataFrame
from shapely import MultiPolygon as ShapelyMultiPolygon
from shapely import Polygon
from utils import Log

log = Log('DNCBase')


class DNCBase:
    def __init__(self, gdf: GeoDataFrame, values: list[float]):
        assert len(gdf) == len(values)
        self.gdf = gdf
        self.values = values

    @staticmethod
    def extract_polygon_base(geometry):
        if isinstance(geometry, Polygon):
            return geometry

        if isinstance(geometry, ShapelyMultiPolygon):
            # TODO: Support MultiPolygon
            return max(
                geometry.geoms,
                key=lambda polygon: polygon.area,
            )

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @staticmethod
    def extract_polygon(geometry, tolerance=0.001):
        polygon = DNCBase.extract_polygon_base(geometry)
        # The simplify method uses the Douglas-Peucker algorithm, which works
        # by iteratively removing points from the shape's boundary until all
        # remaining points are at least tolerance distance away from the
        # original boundary.
        if tolerance > 0:
            polygon = polygon.simplify(tolerance)
        return polygon

    # serializers
    def save_gdf(self, gdf_path):
        self.gdf.to_file(gdf_path, driver='GeoJSON')
        log.info(f'Wrote gdf to {gdf_path}')

    # shapely
    @cached_property
    def polygons(self):
        return [DNCBase.extract_polygon(geo) for geo in self.gdf['geometry']]
