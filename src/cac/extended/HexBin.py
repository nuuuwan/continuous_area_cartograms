import math

from shapely import affinity
from shapely.geometry import Point
from utils import JSONFile, Log

from utils_future import MatPlotLibUser

log = Log("HexBin")


class HexBin(MatPlotLibUser):
    SCALE_FACTOR = 0.9
    N_POLYGON_SIDES = 6
    X_TO_Y_RATIO = math.cos(math.pi / 6)

    def __init__(self, polygons, total_value):
        self.polygons = polygons
        self.total_value = total_value

    @staticmethod
    def get_scaled_polygon(polygon):
        return affinity.scale(
            polygon,
            xfact=HexBin.SCALE_FACTOR,
            yfact=HexBin.SCALE_FACTOR,
            origin=polygon.centroid,
        )

    @staticmethod
    def get_hexagon_centroids_for_polygon(polygon, dim):
        polygon = HexBin.get_scaled_polygon(polygon)
        min_x, min_y, max_x, max_y = polygon.bounds
        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO

        x_min = int(min_x / dim_x) * dim_x
        y_min = int(min_y / dim_y) * dim_y
        point_infos = []
        x = x_min
        r = 0.5 * (dim / math.cos(math.pi / 6) ** 2) / 2

        while x <= max_x:
            y = y_min
            ix = int(x / dim_x)
            if ix % 2 == 0:
                y += dim_y / 4
            else:
                y -= dim_y / 4

            while y <= max_y:
                n_inside = 0
                for i in range(HexBin.N_POLYGON_SIDES):
                    angle = 2 * math.pi / HexBin.N_POLYGON_SIDES * i
                    x1 = x + r * math.cos(angle)
                    y1 = y + r * math.sin(angle)
                    point1 = Point(x1, y1)
                    if polygon.contains(point1):
                        n_inside += 1

                point = Point(x, y)
                if polygon.contains(point):
                    n_inside += 1

                if n_inside > 0:
                    point_infos.append((point, n_inside))

                y += dim_y
            x += dim_x

        return point_infos

    @staticmethod
    def normalize(points_list, dim):
        min_x, min_y, max_x, max_y = None, None, None, None
        for points in points_list:
            for point in points:
                x, y = point.x, point.y
                if min_x is None or x < min_x:
                    min_x = x
                if min_y is None or y < min_y:
                    min_y = y
                if max_x is None or x > max_x:
                    max_x = x
                if max_y is None or y > max_y:
                    max_y = y

        normalized_points_list = []
        for points in points_list:
            normalized_points = []
            for point in points:
                x, y = point.x, point.y
                x = (x - min_x) / dim
                y = 1 - (y - min_y) / dim
                y *= HexBin.X_TO_Y_RATIO * 2

                x = int(round(x, 0))
                y = int(round(y, 0))
                normalized_point = Point(x, y)
                normalized_points.append(normalized_point)
            normalized_points_list.append(normalized_points)
        return normalized_points_list

    def write(self, hexbin_data_path):
        points_list = []

        total_area = sum([polygon.area for polygon in self.polygons])
        dim = round(
            math.sqrt(total_area / self.total_value) * HexBin.SCALE_FACTOR, 3
        )

        idx = {}
        for i_polygon, polygon in enumerate(self.polygons):
            point_infos = HexBin.get_hexagon_centroids_for_polygon(
                polygon,
                dim,
            )
            if len(point_infos) == 0:
                log.error(f"{i_polygon}: No hexagon centroids")

            for point, n_inside in point_infos:
                k = tuple([round(x, 6) for x in point.coords[0]])
                if k not in idx:
                    idx[k] = {}
                idx[k][i_polygon] = n_inside

        i_polygon_to_rem_n_points = {}
        for i_polygon, polygon in enumerate(self.polygons):
            expected_n_points = int(
                round(self.total_value * polygon.area / total_area, 0)
            )
            i_polygon_to_rem_n_points[i_polygon] = expected_n_points

        i_polygon_to_points = {}
        for k, idx2 in sorted(
            idx.items(), key=lambda x: sum(x[1].values()), reverse=True
        ):
            min_rem_i_polygon = None
            for i_polygon, n_inside in sorted(
                idx2.items(), key=lambda x: x[1], reverse=True
            ):
                rem = i_polygon_to_rem_n_points[i_polygon]
                if rem >= 1:
                    min_rem_i_polygon = i_polygon
                    break

            if min_rem_i_polygon is None:
                continue

            if min_rem_i_polygon not in i_polygon_to_points:
                i_polygon_to_points[min_rem_i_polygon] = []
            i_polygon_to_points[min_rem_i_polygon].append(k)
            i_polygon_to_rem_n_points[min_rem_i_polygon] -= 1

        for i_polygon, polygon in enumerate(self.polygons):
            points = []
            for k in i_polygon_to_points.get(i_polygon, []):
                points.append(Point(k))
            points_list.append(points)

        points_list = HexBin.normalize(points_list, dim)

        data = dict(
            points_list=[
                [point.coords[0] for point in points]
                for points in points_list
            ],
            dim=1,
        )
        JSONFile(hexbin_data_path).write(data)
        log.info(f"Wrote {hexbin_data_path}")
