from functools import cached_property

import numpy as np


class DCN1985Properties:
    # Independent of Polygons
    @cached_property
    def total_value(self) -> float:
        return sum(self.values)

    @cached_property
    def Values(self) -> np.ndarray:
        return np.array(self.values)

    @cached_property
    def n_polygons(self):
        return len(self.polygons)

    # Dependent on individual polygons

    @cached_property
    def Point(self) -> np.ndarray:
        return np.array(
            [
                np.array(polygon.exterior.coords, dtype=np.float64)
                for polygon in self.polygons
            ],
            dtype=object,
        )

    @cached_property
    def Centroid(self) -> np.ndarray:
        return np.array(
            [
                np.array(
                    [polygon.centroid.x, polygon.centroid.y], dtype=np.float64
                )
                for polygon in self.polygons
            ]
        )

    @cached_property
    def Area(self) -> np.ndarray:
        return np.array([polygon.area for polygon in self.polygons])

    @cached_property
    def Radius(self) -> np.ndarray:
        return np.sqrt(self.Area / np.pi)

    @cached_property
    def n_points(self):
        return sum(
            [len(polygon.exterior.coords) for polygon in self.polygons]
        )

    # Dependent on all polygons
    @cached_property
    def Desired(self) -> np.ndarray:
        return self.total_area * self.Values / self.total_value

    @cached_property
    def Mass(self) -> np.ndarray:
        return np.sqrt(self.Desired / np.pi) - self.Radius

    @cached_property
    def Error(self) -> np.ndarray:
        return np.max([self.Area, self.Desired], axis=0) / np.min(
            [self.Area, self.Desired], axis=0
        )

    @cached_property
    def Log2Error(self) -> np.ndarray:
        return np.log2(self.Area / self.Desired)

    @cached_property
    def mean_abs_log2_error(self) -> float:
        return np.mean(np.abs(self.Log2Error))

    @cached_property
    def mean_size_error(self) -> float:
        return np.mean(self.Error)

    @cached_property
    def force_reduction_factor(self) -> float:
        return 1 / (1 + self.mean_size_error)

    @cached_property
    def is_reasonably_complete(self) -> bool:
        return np.all(
            np.abs(self.Log2Error) <= self.algo_params.min_log2_error
        )

    @cached_property
    def total_area(self) -> float:
        return sum(self.Area)
