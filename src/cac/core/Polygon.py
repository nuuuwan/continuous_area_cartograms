import math
from functools import cached_property

import numpy as np
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
        return self.shapely_polygon.area

    @cached_property
    def centroid(self):
        return self.shapely_polygon.centroid

    @cached_property
    def radius(self):
        return math.sqrt(self.area / math.pi)

    @cached_property
    def n_points(self):
        return len(self.shapely_polygon.exterior.coords)

    @cached_property
    def np_points(self):
        return np.array(self.shapely_polygon.exterior.coords)
