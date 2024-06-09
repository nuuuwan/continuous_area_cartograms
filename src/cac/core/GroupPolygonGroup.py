from functools import cached_property

from utils import Log

log = Log('GroupPolygonGroup')


class GroupPolygonGroup:
    def __init__(self, grouped_polygons):
        self.grouped_polygons = grouped_polygons

    @cached_property
    def mean_size_error(self):
        s = sum(
            grouped_polygon.size_error
            for grouped_polygon in self.grouped_polygons
        )
        n = len(self.grouped_polygons)
        return s / n

    @cached_property
    def force_reduction_factor(self):
        # "ForceReductionFactor = 1 / (1 + Mean (SizeError))"
        return 1 / (1 + self.mean_size_error)
