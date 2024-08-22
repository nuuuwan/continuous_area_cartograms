import math

from shapely import affinity
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union
from utils import JSONFile, Log

from algos_future import Hungarian

log = Log("HexBin")


class HexBin:
    SCALE_FACTOR = 1
    N_POLYGON_SIDES = 6
    X_TO_Y_RATIO = math.cos(math.pi / 6)

    def __init__(
        self,
        polygons,
        values,
        total_value,
        labels,
        label_to_group,
        post_process,
    ):
        self.polygons = polygons
        self.values = values
        self.total_value = total_value
        self.labels = labels
        self.label_to_group = label_to_group
        self.post_process = post_process

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
        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO
        r = (dim / math.cos(math.pi / 6) ** 2) / 2

        polygon = HexBin.get_scaled_polygon(polygon)
        min_x, min_y, max_x, max_y = polygon.bounds
        PADDING = 1
        x_min = int(min_x / dim_x - PADDING) * dim_x
        y_min = int(min_y / dim_y - PADDING) * dim_y

        point_infos = []
        ix = 0
        while True:
            x = x_min + ix * dim_x
            if x > max_x + PADDING * dim_x:
                break
            is_odd = (int(round(x / dim_x, 0)) % 2) == 1

            iy = 0
            while True:
                y = y_min + iy * dim_y
                if is_odd:
                    y -= dim_y / 4
                else:
                    y += dim_y / 4
                if y > max_y + PADDING * dim_y:
                    break

                n_inside = 0
                for k in [0.125, 0.25, 0.5, 1]:
                    for i in range(HexBin.N_POLYGON_SIDES):
                        angle = 2 * math.pi / HexBin.N_POLYGON_SIDES * i
                        x1 = x + k * r * math.cos(angle)
                        y1 = y + k * r * math.sin(angle)
                        point1 = Point(x1, y1)
                        if polygon.contains(point1):
                            n_inside += 1 / k

                point = Point(x, y)

                if polygon.contains(point):
                    n_inside += 32

                if n_inside > 0:
                    point_infos.append((point, n_inside))

                iy += 1
            ix += 1

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

        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO

        normalized_points_list = []
        for points in points_list:
            normalized_points = []
            for point in points:
                x, y = point.x, point.y
                x = (x - min_x) / dim_x
                y = (max_y - y) / dim_y

                x = round(x, 2)
                y = round(y, 2)
                normalized_point = Point(x, y)
                normalized_points.append(normalized_point)
            normalized_points_list.append(normalized_points)
        return normalized_points_list

    @staticmethod
    def get_polygon(point, dim, expand_factor=1.0):
        x, y = point.x, point.y

        r = expand_factor * (dim / math.cos(math.pi / 6) ** 2) / 2
        points = []
        for i in range(HexBin.N_POLYGON_SIDES):
            angle = 2 * math.pi / HexBin.N_POLYGON_SIDES * i
            x1 = x + r * math.cos(angle)
            y1 = y + r * math.sin(angle)

            points.append(Point(x1, y1))
        return Polygon(points)

    @staticmethod
    def get_group_polygons(points, dim):
        polygons = []
        for point in points:
            polygons.append(
                HexBin.get_polygon(point, dim, expand_factor=1.001)
            )
        combined = unary_union(polygons)

        polygons = []
        if isinstance(combined, Polygon):
            polygons = [combined]
        elif not isinstance(combined, MultiPolygon):
            polygons = list(combined.geoms)
        else:
            polygons = []

        return polygons

    def build(
        self,
    ):
        total_area = sum([polygon.area for polygon in self.polygons])
        dim = (
            math.sqrt(total_area)
            * HexBin.SCALE_FACTOR
            / math.sqrt(self.total_value)
        )

        p_to_k_to_n = {}
        k_set = set()
        for i_polygon, polygon in enumerate(self.polygons):
            point_infos = HexBin.get_hexagon_centroids_for_polygon(
                polygon,
                dim,
            )
            if len(point_infos) == 0:
                log.error(f"{i_polygon}: No hexagon centroids")

            for point, n_inside in point_infos:
                k = tuple([round(x, 6) for x in point.coords[0]])
                k_set.add(k)
                if i_polygon not in p_to_k_to_n:
                    p_to_k_to_n[i_polygon] = {}
                p_to_k_to_n[i_polygon][k] = n_inside
        sorted_ks = sorted(list(k_set))

        cost_matrix = []
        INF = float("inf")
        total_value = sum(self.values)
        for i_polygon, polygon in enumerate(self.polygons):
            n_points_exp = int(
                round(
                    self.total_value * self.values[i_polygon] / total_value, 0
                )
            )
            k_to_n = p_to_k_to_n[i_polygon]

            for j in range(n_points_exp):
                row = []
                for k in sorted_ks:
                    cost = INF
                    if k in k_to_n:
                        cost = 1.0 / k_to_n[k]
                    row.append(cost)
                cost_matrix.append(row)

        optimal_assignment = Hungarian(cost_matrix).run()

        points_list = []
        ij_to_ik = dict(optimal_assignment)
        k_set = set()
        ij = 0
        for i_polygon, polygon in enumerate(self.polygons):
            n_points_exp = int(
                round(
                    self.total_value * self.values[i_polygon] / total_value, 0
                )
            )
            points = []
            for j in range(n_points_exp):
                ik = ij_to_ik[ij]
                ij += 1
                k = sorted_ks[ik]
                if k in k_set:
                    log.error(f"Duplicate k: {k}")
                k_set.add(k)
                points.append(Point(k))
            points_list.append(points)

        points_list = HexBin.normalize(points_list, dim)
        idx = dict(
            zip(
                self.labels,
                [
                    [list(point.coords[0]) for point in points]
                    for points in points_list
                ],
            )
        )
        if self.post_process:
            idx = self.post_process(dict(idx=idx))['idx']

        group_to_points = {}
        for label, points in idx.items():
            group = self.label_to_group[label]
            if group not in group_to_points:
                group_to_points[group] = []
            group_to_points[group].extend(points)

        idx2 = {}
        for group, points in group_to_points.items():
            polygons = HexBin.get_group_polygons(
                [
                    Point(point[0], point[1] / HexBin.X_TO_Y_RATIO)
                    for point in points
                ],
                1,
            )
            idx2[group] = [
                [
                    (point[0], point[1] * HexBin.X_TO_Y_RATIO)
                    for point in polygon.exterior.coords
                ]
                for polygon in polygons
            ]

        return dict(
            idx=idx,
            idx2=idx2,
            dim=1,
        )

    @staticmethod
    def validate(data):
        idx = data['idx']
        duplicate_idx = {}
        for label, points in idx.items():
            for point in points:
                point = tuple(point)
                if point in duplicate_idx:
                    log.error(
                        f"{point}: '{label}' Duplicated with {duplicate_idx[point]}"
                    )
                if point not in duplicate_idx:
                    duplicate_idx[point] = []
                duplicate_idx[point].append(label)

        n = len(idx.keys())
        log.warn(f'{n=}')

    def write(self, hexbin_data_path):
        data = self.build()
        self.validate(data)
        JSONFile(hexbin_data_path).write(data)
        log.info(f"Wrote {hexbin_data_path}")
