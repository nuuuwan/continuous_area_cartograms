import os
import shutil
import tempfile
import time

import numpy as np
from shapely import Polygon
from utils import Log

from utils_future import AnimatedGIF

log = Log('DNCRunner')


class DNCRunner:
    MAX_ITERATIONS = 10

    @staticmethod
    def run_single_optimized(dnc):
        force_reduction_factor = dnc.force_reduction_factor
        Centroid = dnc.Centroid
        Radius = dnc.Radius
        Mass = dnc.Mass
        Point = dnc.Point

        new_Point = []
        for Point_i in Point:
            Delta_i = Point_i[np.newaxis, :, :] - Centroid[:, np.newaxis, :]
            Distance_i = np.linalg.norm(Delta_i, axis=2).transpose()
            Angle_i = np.arctan2(
                Delta_i[:, :, 1], Delta_i[:, :, 0]
            ).transpose()

            Point_i += (
                np.sum(
                    np.where(
                        Distance_i > Radius,
                        Mass * (Radius / Distance_i),
                        Mass
                        * (Distance_i**2 / Radius**2)
                        * (4 - 3 * (Distance_i / Radius)),
                    )
                    * np.array([np.cos(Angle_i), np.sin(Angle_i)]),
                    axis=2,
                ).transpose()
                * force_reduction_factor
            )

            new_Point.append(Point_i)

        polygons = [Polygon(Point_i) for Point_i in new_Point]
        return dnc.__class__.from_dnc(dnc, polygons)

    @staticmethod
    def run_all(dnc0, dir_output):
        cls = dnc0.__class__
        dnc = dnc0
        dnc.log_complexity()

        i_iter = 0
        t_start = time.time()
        dir_image = os.path.join(dir_output, 'images')

        while True:
            t_lap_start = time.time()

            # save image
            file_id = f'{i_iter:03}'
            image_path = os.path.join(dir_image, f'{file_id}.png')
            dnc.save_image(image_path)

            # save gdf
            gdf_path = os.path.join(dir_output, 'geojson', f'{file_id}.json')
            dnc.save_gdf(gdf_path)

            dnc.log_error()
            if dnc.is_reasonably_complete:
                break
            dnc = cls.run_single_optimized(dnc)

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

        AnimatedGIF(os.path.join(dir_output, 'animated.gif')).write(dir_image)

        return dnc

    def run(self, dir_output=None):
        if dir_output is None:
            dir_output = tempfile.mkdtemp()
        else:
            shutil.rmtree(dir_output, ignore_errors=True)
            os.makedirs(dir_output, exist_ok=True)

        for child_dir_name in ['geojson', 'images']:
            os.makedirs(
                os.path.join(dir_output, child_dir_name), exist_ok=True
            )

        return self.__class__.run_all(self, dir_output)
