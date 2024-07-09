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
        # polygons
        self.polygons = [
            DCN1985Base.preprocess(polygon, tolerance=preprocess_tolerance)
            for polygon in polygons
        ]

        # values
        if values is None:
            values = [1 for _ in range(len(polygons))]
        self.values = values

        # labels
        if labels is None:
            labels = [str(i) for i in range(len(polygons))]
        self.labels = labels

        # validations
        assert len(self.polygons) == len(self.values) == len(self.labels)

        # optional options
        log.debug(
            dict(
                preprocess_tolerance=preprocess_tolerance,
                min_log2_error=min_log2_error,
                max_iterations=max_iterations,
                do_shrink=do_shrink,
                title=title,
                area_unit=area_unit,
                value_unit=value_unit,
                true_total_area=true_total_area,
            )
        )
        self.preprocess_tolerance = preprocess_tolerance
        self.min_log2_error = min_log2_error
        self.max_iterations = max_iterations
        self.do_shrink = do_shrink

        # area labels
        self.title = title
        self.area_unit = area_unit
        self.value_unit = value_unit
        self.true_total_area = true_total_area

    @staticmethod
    def preprocess(polygon, tolerance):
        # The simplify method uses the Douglas-Peucker algorithm, which works
        # by iteratively removing points from the shape's boundary until all
        # remaining points are at least tolerance distance away from the
        # original boundary.
        if tolerance > 0:
            polygon = polygon.simplify(tolerance=tolerance)
        return polygon
