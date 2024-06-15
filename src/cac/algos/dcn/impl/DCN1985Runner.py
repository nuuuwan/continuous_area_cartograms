import os
import shutil
import tempfile
import time

import numpy as np
from shapely import Polygon, affinity
from utils import Log

from utils_future import AnimatedGIF

log = Log('DCN1985Runner')


class DCN1985Runner:
    @classmethod
    def run_single_optimized(cls, dcn):
        force_reduction_factor = dcn.force_reduction_factor
        Centroid = dcn.Centroid
        Radius = dcn.Radius
        Mass = dcn.Mass
        Point = dcn.Point

        new_Point = []
        for Point_i in Point:
            Delta_i = np.array(
                Point_i[np.newaxis, :, :] - Centroid[:, np.newaxis, :],
                dtype=np.float64,
            )
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
        dcn = dcn.from_dcn(polygons)
        return dcn

    @classmethod
    def shrink(cls, dcn, min_p=1, shrink_factor=0.1):
        new_polygons = []
        total_area = dcn.total_area
        total_value = dcn.total_value
        for polygon, value in zip(dcn.polygons, dcn.values):
            p = (value / total_value) / (polygon.area / total_area)
            if p < min_p:
                scale_factor = p**shrink_factor
                polygon = affinity.scale(polygon, scale_factor, scale_factor)
            new_polygons.append(polygon)
        return dcn.from_dcn(new_polygons)

    @classmethod
    def run_all(cls, dcn0, dir_output):
        dcn = dcn0
        dcn.log_complexity()

        i_iter = 0
        t_start = time.time()
        dir_image = os.path.join(dir_output, 'images')

        while True:
            t_lap_start = time.time()

            # save image
            file_id = f'{i_iter:03}'
            image_path = os.path.join(dir_image, f'{file_id}.png')
            dcn.save_image(image_path)

            # save gdf
            gdf_path = os.path.join(dir_output, 'geojson', f'{file_id}.json')
            dcn.to_gdf().to_file(gdf_path, driver='GeoJSON')

            dcn.log_error()
            if dcn.is_reasonably_complete:
                break
            dcn = cls.run_single_optimized(dcn)
            if dcn.do_shrink:
                dcn = cls.shrink(
                    dcn,
                    min_p=i_iter / dcn.max_iterations,
                    shrink_factor=i_iter / dcn.max_iterations,
                )

            t_now = time.time()
            dt_all = t_now - t_start
            dt_iter = t_now - t_lap_start
            log.debug(f'⏱️{i_iter=}, {dt_all=:.2f}s, {dt_iter=:.2f}s')
            i_iter += 1
            if i_iter >= dcn.max_iterations:
                log.warning(f'MAX_ITERATIONS({dcn.max_iterations}) reached.')
                break

        AnimatedGIF(os.path.join(dir_output, 'animated.gif')).write(dir_image)

        return dcn.polygons

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
