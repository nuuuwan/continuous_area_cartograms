import math
import os
import tempfile
import time

from shapely import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from utils import Log

from utils_future import AnimatedGIF

log = Log('DNCRunner')


class DNCRunner:
    @staticmethod
    def run_single(dnc):  # noqa
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

    @classmethod
    def save_image_for_iter(cls, dnc, dir_output, i_iter):
        image_path = os.path.join(dir_output, f'{i_iter}.png')
        cls.save_image(
            dnc.grouped_polygons,
            image_path,
        )
        return image_path

    @classmethod
    def build_new_dnc(cls, dnc, shapely_polygons):
        ids = list(dnc.id_to_shapely_polygons.keys())
        id_to_shapely_polygons = {
            id: shapely_polygon
            for id, shapely_polygon in zip(ids, shapely_polygons)
        }
        return cls(id_to_shapely_polygons, dnc.id_to_value)

    @staticmethod
    def save_animated_gif(image_path_list, dir_output):
        animated_gif_path = os.path.join(dir_output, 'animated.gif')
        AnimatedGIF(animated_gif_path).write(image_path_list)

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
            image_path = cls.save_image_for_iter(dnc, dir_output, i_iter)
            image_path_list.append(image_path)

            dnc.log_error()
            if dnc.grouped_polygon_group.is_reasonably_complete:
                break

            shapely_polygons = cls.run_single(dnc)
            dnc = cls.build_new_dnc(dnc, shapely_polygons)

            t_now = time.time()
            dt_all = t_now - t_start
            dt_iter = t_now - t_lap_start
            log.debug(f'⏱️{i_iter=}, {dt_all=:.2f}s, {dt_iter=:.2f}s')
            i_iter += 1

        DNCRunner.save_animated_gif(image_path_list, dir_output)
        return dnc

    def run(self, dir_output=None):
        if dir_output is None:
            dir_output = tempfile.mkdtemp()
        else:
            os.makedirs(dir_output, exist_ok=True)
        self.__class__.run_all(self, dir_output)
