import math
import os

from shapely import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from utils import Log

from utils_future import AnimatedGIF

log = Log('DNCRunner')


class DNCRunner:
    def run_single(self):
        # "For each boundary line; Read coordinate chain"
        #     "For each coordinate pair"
        new_shapely_polygons = []

        self.log_error()

        for polygon in self.grouped_polygons:
            new_points = []
            point_set = set()
            for point in polygon.shapely_polygon.exterior.coords:
                # Don't repeat points already processed
                if point in point_set:
                    continue
                point_set.add(point)
                dx, dy = 0, 0
                # "For each polygon centroid"
                for polygon0 in self.grouped_polygons:
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
                    frf = self.group_polygon_group.force_reduction_factor

                    k = frf * fij
                    dx += k * math.cos(angle)
                    dy += k * math.sin(angle)
                # Move coordinate accordingly
                new_point = (point[0] + dx, point[1] + dy)
                new_points.append(new_point)
            new_shapely_polygon = ShapelyPolygon(new_points)
            new_shapely_polygons.append(new_shapely_polygon)

        return new_shapely_polygons

    
    def run(self, file_label, n_iterations=1):
        cls = self.__class__
        assert file_label
        assert n_iterations > 0

        dir_path = os.path.join(
            'images',
            file_label,
        )
        os.makedirs(dir_path, exist_ok=True)

        dnc = self
        shapely_polygons = list(dnc.id_to_shapely_polygons.values())
        image_path_list = []
        # "For each iteration (user controls when done)"
        for i_iteration in range(n_iterations):
            log.debug(f'run: {i_iteration=}')

            image_path = os.path.join(dir_path, f'{i_iteration}.png')
            cls.save_image(
                dnc.grouped_polygons,
                image_path,
            )
            image_path_list.append(image_path)

            shapely_polygons = dnc.run_single()
            ids = list(dnc.id_to_shapely_polygons.keys())
            id_to_shapely_polygons = {
                id: shapely_polygon
                for id, shapely_polygon in zip(ids, shapely_polygons)
            }
            dnc = cls(id_to_shapely_polygons, dnc.id_to_value)

        image_path = os.path.join(dir_path, f'{n_iterations}.png')
        cls.save_image(
            dnc.grouped_polygons,
            image_path,
        )
        image_path_list.append(image_path)

        animated_gif_path = os.path.join(dir_path, 'animated.gif')
        AnimatedGIF(animated_gif_path).write(image_path_list)

        return shapely_polygons
