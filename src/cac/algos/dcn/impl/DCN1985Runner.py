import numpy as np
from shapely import Polygon, affinity
from utils import Log

log = Log('DCN1985Runner')


class DCN1985Runner:
    @staticmethod
    def get_Delta_i(Point_i, Centroid):
        return np.array(
            Point_i[np.newaxis, :, :] - Centroid[:, np.newaxis, :],
            dtype=np.float64,
        )

    @staticmethod
    def get_Point_i_incr(
        Distance_i, Radius, Mass, Angle_i, force_reduction_factor
    ):
        return (
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

    @classmethod
    def run_single_optimized(cls, dcn):
        force_reduction_factor = dcn.force_reduction_factor
        Centroid = dcn.Centroid
        Radius = dcn.Radius
        Mass = dcn.Mass
        Point = dcn.Point

        new_Point = []
        for Point_i in Point:
            Delta_i = DCN1985Runner.get_Delta_i(Point_i, Centroid)
            Distance_i = np.linalg.norm(Delta_i, axis=2).transpose()
            Angle_i = np.arctan2(
                Delta_i[:, :, 1], Delta_i[:, :, 0]
            ).transpose()
            Point_i += DCN1985Runner.get_Point_i_incr(
                Distance_i, Radius, Mass, Angle_i, force_reduction_factor
            )
            new_Point.append(Point_i)
        polygons = []
        for Point_i in new_Point:
            try:
                polygons.append(Polygon(Point_i))
            except Exception as e:
                log.error(f'Could not append polygon: {e}')
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
        dcn_list = []

        dcn0.log_complexity()
        dcn = dcn0
        i_iter = 0
        while True:
            dcn_list.append(dcn)
            dcn.log_error()
            if dcn.is_reasonably_complete:
                break
            dcn = cls.run_single_optimized(dcn)
            if dcn.algo_params.do_shrink:
                dcn = cls.shrink(
                    dcn,
                    min_p=i_iter / dcn.algo_params.max_iterations,
                    shrink_factor=i_iter / dcn.algo_params.max_iterations,
                )

            i_iter += 1
            if i_iter >= dcn.algo_params.max_iterations:
                log.warning(
                    f'🛑 max_iterations({dcn.algo_params.max_iterations})'
                    + ' reached.'
                )
                break

        return dcn_list
