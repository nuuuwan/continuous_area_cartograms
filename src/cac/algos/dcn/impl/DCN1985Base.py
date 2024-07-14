from shapely import Polygon
from utils import Log

from cac.algos.dcn.impl.DCN1985AlgoParams import DCN1985AlgoParams
from cac.algos.dcn.impl.DCN1985RenderParams import DCN1985RenderParams

log = Log('DCN1985Base')


class DCN1985Base:
    def __init__(
        self,
        polygons: list[Polygon],
        values=None,
        labels=None,
        algo_params=None,
        render_params=None,
    ):
        self.algo_params = algo_params or DCN1985AlgoParams()
        self.render_params = render_params or DCN1985RenderParams()

        self.polygons = DCN1985Base.preprocess_polygons(
            polygons, tolerance=self.algo_params.preprocess_tolerance
        )
        self.values = values
        self.labels = labels or [str(i) for i in range(len(polygons))]

        self.validate()


    def validate(self):
        assert len(self.polygons) == len(
            self.values
        ), f'{len(self.polygons)} != {len(self.values)}'
        assert len(self.polygons) == len(
            self.labels
        ), f'{len(self.polygons)} != {len(self.labels)}'

    @staticmethod
    def preprocess_polygons(polygons, tolerance):
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

    def __hash__(self):
        return hash(
            dict(
                polygons=self.polygons,
                values=self.values,
                algo_params=self.algo_params,
            )
        )
