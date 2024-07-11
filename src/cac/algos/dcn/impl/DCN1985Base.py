from shapely import Polygon
from utils import Log

log = Log('DCN1985Base')


class DCN1985Base:
    def __init__(
        self,
        polygons: list[Polygon],
        values=None,
        labels=None,
        preprocess_tolerance=0.001,
        min_log2_error=0.1,
        max_iterations=30,
        do_shrink=False,
        title='',
        area_unit="area (%)",
        value_unit="value",
        true_total_area=100,
    ):
        self.polygons = DCN1985Base.proprocess_polygons(
            polygons, tolerance=preprocess_tolerance
        )

        self.values = values
        self.labels = labels or [str(i) for i in range(len(polygons))]

        # params
        self.preprocess_tolerance = preprocess_tolerance
        self.min_log2_error = min_log2_error
        self.max_iterations = max_iterations
        self.do_shrink = do_shrink

        # area labels
        self.title = title
        self.area_unit = area_unit
        self.value_unit = value_unit
        self.true_total_area = true_total_area

        self.validate()

    def validate(self):
        assert len(self.polygons) == len(self.values) == len(self.labels)

    @staticmethod
    def proprocess_polygons(polygons, tolerance):
        return [
            DCN1985Base.preprocess_polygon(polygon, tolerance=tolerance)
            for polygon in polygons
        ]

    @staticmethod
    def preprocess_polygon(polygon, tolerance):
        # The simplify method uses the Douglas-Peucker algorithm, which works
        # by iteratively removing points from the shape's boundary until all
        # remaining points are at least tolerance distance away from the
        # original boundary.
        if tolerance > 0:
            polygon = polygon.simplify(tolerance=tolerance)
        return polygon
