import math
from functools import cached_property

from utils import Log

log = Log('Polygon')


class Polygon:
    def __init__(
        self,
        id,
        shapely_polygon,
        value,
    ):
        self.id = id
        self.shapely_polygon = shapely_polygon
        self.value = value

    @cached_property
    def area(self):
        # "Calculate area and centroid (using current boundaries) (1)"
        return self.shapely_polygon.area

    @cached_property
    def centroid(self):
        # "Calculate area and centroid (using current boundaries) (2)"
        return self.shapely_polygon.centroid

    @cached_property
    def radius(self):
        # "Radius = √ (Area/pi)"
        return math.sqrt(self.area / math.pi)
