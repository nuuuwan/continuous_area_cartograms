import os
import tempfile
import time

import numpy as np
from shapely import Polygon as ShapelyPolygon
from utils import Log

from utils_future import AnimatedGIF

log = Log('DNCRunner')


class DNCRunner:
    MAX_ITERATIONS = 30

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
            if i_iter >= DNCRunner.MAX_ITERATIONS:
                log.warning(
                    f'MAX_ITERATIONS({DNCRunner.MAX_ITERATIONS}) reached.'
                )
                break

        animated_gif_path = os.path.join(dir_output, 'animated.gif')
        AnimatedGIF(animated_gif_path).write(image_path_list)
        return dnc

    def run(self, dir_output=None):
        if dir_output is None:
            dir_output = tempfile.mkdtemp()
        else:
            os.makedirs(dir_output, exist_ok=True)
        self.__class__.run_all(self, dir_output)
