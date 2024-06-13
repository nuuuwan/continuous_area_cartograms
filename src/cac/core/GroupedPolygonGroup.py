from functools import cached_property
import numpy as np
from utils import Log

log = Log('GroupedPolygonGroup')


class GroupedPolygonGroup:
    MIN_ABS_LOG2_ERROR_FOR_COMPLETION = 0.1

    def __init__(self, grouped_polygons):
        self.grouped_polygons = grouped_polygons

    @cached_property
    def E(self) -> np.ndarray:
        return np.array([
            grouped_polygon.size_error
            for grouped_polygon in self.grouped_polygons
        ])

    @cached_property
    def mean_size_error(self) -> float:
        return np.mean(self.E)

    @cached_property
    def force_reduction_factor(self)-> float:
        print(self.mean_size_error)
        return 1 / (1 + self.mean_size_error)

    @cached_property
    def is_reasonably_complete(self) -> bool:
        for grouped_polygon in self.grouped_polygons:
            log2_error = grouped_polygon.log2_error
            if abs(log2_error) > self.MIN_ABS_LOG2_ERROR_FOR_COMPLETION:
                return False
        return True
