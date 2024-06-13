from shapely import Polygon
from utils import Log

log = Log('DNCBase')


class DNCBase:
    def __init__(self, polygons: list[Polygon], values: list[float]):
        assert len(polygons) == len(values)
        self.polygons = [DNCBase.preprocess(polygon) for polygon in polygons]
        self.values = values

    @staticmethod
    def preprocess(polygon, tolerance=0.001):
        # The simplify method uses the Douglas-Peucker algorithm, which works
        # by iteratively removing points from the shape's boundary until all
        # remaining points are at least tolerance distance away from the
        # original boundary.
        if tolerance > 0:
            polygon = polygon.simplify(tolerance=tolerance)
        return polygon
