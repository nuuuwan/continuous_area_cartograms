from functools import cached_property

from utils import Log

log = Log('PolygonGroup')


class PolygonGroup:
    def __init__(self, polygons):
        self.polygons = polygons

    @cached_property
    def total_area(self):
        # "Sum areas into TotalArea"
        return sum(polygon.area for polygon in self.polygons)

    @cached_property
    def total_value(self):
        # "Sum PolygonValue into TotalValue"
        return sum(polygon.value for polygon in self.polygons)

    @cached_property
    def n_polygons(self):
        return len(self.polygons)

    @cached_property
    def n_points(self):
        return sum(polygon.n_points for polygon in self.polygons)
