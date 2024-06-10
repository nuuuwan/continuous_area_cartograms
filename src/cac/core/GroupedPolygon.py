import math
from functools import cached_property

from utils import Log

from cac.core.Polygon import Polygon
from cac.core.PolygonGroup import PolygonGroup

log = Log('GroupedPolygon')


class GroupedPolygon(Polygon, PolygonGroup):
    def __init__(self, polygon, polygon_group):
        Polygon.__init__(
            self, polygon.id, polygon.shapely_polygon, polygon.value
        )
        PolygonGroup.__init__(self, polygon_group.polygons)

    @cached_property
    def desired(self):
        # "Desired = (TotalArea * (PolygonValue / TotalValue))"
        return self.total_area * self.value / self.total_value

    @cached_property
    def mass(self):
        # Mass = √ (Desired / 𝜋) - √ (Area / 𝜋)
        return math.sqrt(self.desired / math.pi) - self.radius

    @cached_property
    def size_error(self):
        # "SizeError = Max(Area, Desired) / Min(Area, Desired)"
        return max(self.area, self.desired) / min(self.area, self.desired)

    @cached_property
    def log2_error(self):
        e = self.area / self.desired
        return math.log2(e)

    @cached_property
    def actual(self):
        return self.value * self.area / self.desired
