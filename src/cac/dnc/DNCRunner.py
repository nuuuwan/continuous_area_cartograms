import math
import os
import tempfile
import time

import numpy as np
from shapely import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from utils import Log

from utils_future import AnimatedGIF

log = Log('DNCRunner')


class DNCRunner:
    @staticmethod
    def run_single_optimized(dnc):
        # all
        frf = dnc.grouped_polygon_group.force_reduction_factor

        # h (polygons in map)
        C = np.array(
            [
                np.array([polygon0.centroid.x, polygon0.centroid.y])
                for polygon0 in dnc.grouped_polygons
            ]
        )
        R = np.array([polygon0.radius for polygon0 in dnc.grouped_polygons])
        M = np.array([polygon0.mass for polygon0 in dnc.grouped_polygons])

        P = np.array(
            [polygon.np_points for polygon in dnc.grouped_polygons],
            dtype=object,
        )

        newP = []
        for Pi in P:  # i (polygons to modify)
            T_i = Pi[np.newaxis, :, :] - C[:, np.newaxis, :]
            D_i = np.linalg.norm(T_i, axis=2).transpose()
            A_i = np.arctan2(T_i[:, :, 1], T_i[:, :, 0]).transpose()

            Pi += (
                np.sum(
                    np.where(
                        D_i > R,
                        M * (R / D_i),
                        M * (D_i**2 / R**2) * (4 - 3 * (D_i / R)),
                    )
                    * np.array([np.cos(A_i), np.sin(A_i)]),
                    axis=2,
                ).transpose()
                * frf
            )

            newP.append(Pi)

        return [ShapelyPolygon(Pi) for Pi in newP]

    @staticmethod
    @DeprecationWarning
    def run_single_legacy(dnc):  # noqa
        # "For each boundary line; Read coordinate chain"
        #     "For each coordinate pair"
        new_shapely_polygons = []

        for polygon in dnc.grouped_polygons:
            new_points = []
            point_set = set()
            for point in polygon.shapely_polygon.exterior.coords:
                # Don't repeat points already processed
                if point in point_set:
                    continue
                point_set.add(point)
                dx, dy = 0, 0
                # "For each polygon centroid"
                for polygon0 in dnc.grouped_polygons:
                    centroid0 = polygon0.centroid

                    # "Find angle, Distance from centroid to coordinate"
                    distance = centroid0.distance(ShapelyPoint(point))
                    angle = math.atan2(
                        point[1] - centroid0.y, point[0] - centroid0.x
                    )
                    # "If (Distance > Radius of polygon)"
                    if distance > polygon0.radius:
                        # "Fij = Mas * (Radius / Distance)"
                        fij = polygon0.mass * (polygon0.radius / distance)
                    # "Else"
                    else:
                        # "Fij = Mass * (Distance² / Radius²)
                        #     * (4 - 3 * (Distance / Radius))"
                        q = distance / polygon0.radius
                        fij = polygon0.mass * (q**2) * (4 - 3 * q)

                    # "Using Fij and angles, calculate vector sum"
                    # "Multiply by ForceReductionFactor"
                    frf = dnc.grouped_polygon_group.force_reduction_factor

                    k = frf * fij
                    dx += k * math.cos(angle)
                    dy += k * math.sin(angle)
                # Move coordinate accordingly
                new_point = (point[0] + dx, point[1] + dy)
                new_points.append(new_point)
            new_shapely_polygon = ShapelyPolygon(new_points)
            new_shapely_polygons.append(new_shapely_polygon)

        return new_shapely_polygons

    @staticmethod
    def run_all(dnc0, dir_output):
        cls = dnc0.__class__
        dnc = dnc0
        dnc.log_complexity()
        shapely_polygons = list(dnc.id_to_shapely_polygons.values())
        image_path_list = []
        i_iter = 0
        # "For each iteration (user controls when done)"
        t_start = time.time()
        while True:
            t_lap_start = time.time()
            image_path = os.path.join(dir_output, f'{i_iter}.png')
            image_path = dnc.save_image(image_path)
            image_path_list.append(image_path)

            dnc.log_error()
            if dnc.grouped_polygon_group.is_reasonably_complete:
                break

            shapely_polygons = cls.run_single_optimized(dnc)
            dnc = cls.from_dnc(dnc, shapely_polygons)

            t_now = time.time()
            dt_all = t_now - t_start
            dt_iter = t_now - t_lap_start
            log.debug(f'⏱️{i_iter=}, {dt_all=:.2f}s, {dt_iter=:.2f}s')
            i_iter += 1

        animated_gif_path = os.path.join(dir_output, 'animated.gif')
        AnimatedGIF(animated_gif_path).write(image_path_list)
        return dnc

    def run(self, dir_output=None):
        if dir_output is None:
            dir_output = tempfile.mkdtemp()
        else:
            os.makedirs(dir_output, exist_ok=True)
        self.__class__.run_all(self, dir_output)
