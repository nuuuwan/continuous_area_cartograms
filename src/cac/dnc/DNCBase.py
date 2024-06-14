from shapely import Polygon
from utils import Log

log = Log('DNCBase')


class DNCBase:
    def __init__(
        self,
        polygons: list[Polygon],
        values: list[float],
        preprocess_tolerance=0.001,
        min_log2_error=0.1,
        max_iterations=30,
    ):
        assert len(polygons) == len(values)
        self.polygons = [
            DNCBase.preprocess(polygon, tolerance=preprocess_tolerance)
            for polygon in polygons
        ]
        self.values = values

        # optional options
        log.debug(
            dict(
                preprocess_tolerance=preprocess_tolerance,
                min_log2_error=min_log2_error,
                max_iterations=max_iterations,
            )
        )
        self.preprocess_tolerance = preprocess_tolerance
        self.min_log2_error = min_log2_error
        self.max_iterations = max_iterations

    @staticmethod
    def preprocess(polygon, tolerance):
        # The simplify method uses the Douglas-Peucker algorithm, which works
        # by iteratively removing points from the shape's boundary until all
        # remaining points are at least tolerance distance away from the
        # original boundary.
        if tolerance > 0:
            polygon = polygon.simplify(tolerance=tolerance)
        return polygon
