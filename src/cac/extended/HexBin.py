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
    PADDING = 1

    def __init__(
        self,
        polygons,
        values,
        total_value,
        labels,
        group_label_to_group,
        post_process,
    ):
        self.polygons = polygons
        self.values = values
        self.total_value = total_value
        self.labels = labels
        self.group_label_to_group = group_label_to_group
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
    def get_n_inside(polygon, x, y, r):
        n_inside = 0
        for k in [0.125, 0.25, 0.5, 1, 2]:
            for i in range(HexBin.N_POLYGON_SIDES):
                angle = 2 * math.pi / HexBin.N_POLYGON_SIDES * i
                x1 = x + k * r * math.cos(angle)
                y1 = y + k * r * math.sin(angle)
                if polygon.contains(Point(x1, y1)):
                    n_inside += 1 / k
        return n_inside

    @staticmethod
    def get_hexagon_centroids_for_polygon(polygon, dim):

        polygon = HexBin.get_scaled_polygon(polygon)
        min_x, min_y, max_x, max_y = polygon.bounds

        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO
        x_min = int(min_x / dim_x - HexBin.PADDING) * dim_x
        y_min = int(min_y / dim_y - HexBin.PADDING) * dim_y
        r = (dim / math.cos(math.pi / 6) ** 2) / 2

        point_infos = []
        for ix in range(
            0, int((max_x + HexBin.PADDING * dim_x - x_min) / dim_x) + 1
        ):
            x = x_min + ix * dim_x
            is_odd = (int(round(x / dim_x, 0)) % 2) == 1
            for iy in range(
                0, int((max_y + HexBin.PADDING * dim_y - y_min) / dim_y) + 1
            ):
                y = y_min + iy * dim_y + dim_y * 0.25 * (-1 if is_odd else 1)

                n_inside = HexBin.get_n_inside(polygon, x, y, r)

                point = Point(x, y)
                if polygon.contains(point):
                    n_inside += 32
                if n_inside > 0:
                    point_infos.append((point, n_inside))

        return point_infos

    @staticmethod
    def get_bbox(points_list):
        min_x, min_y, max_x, max_y = None, None, None, None
        for points in points_list:
            for point in points:
                x, y = point.x, point.y
                min_x = x if min_x is None else min(min_x, x)
                min_y = y if min_y is None else min(min_y, y)
                max_x = x if max_x is None else max(max_x, x)
                max_y = y if max_y is None else max(max_y, y)

        return min_x, min_y, max_x, max_y

    @staticmethod
    def normalize(points_list, dim):
        min_x, __, __, max_y = HexBin.get_bbox(points_list)
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
            polygons.append(HexBin.get_polygon(point, dim, expand_factor=1.01))
        combined = unary_union(polygons)

        polygons = []
        if isinstance(combined, Polygon):
            polygons = [combined]
        elif not isinstance(combined, MultiPolygon):
            polygons = list(combined.geoms)
        else:
            polygons = []

        return polygons

    def get_cost_matrix(self, p_to_k_to_n, sorted_ks):
        cost_matrix = []
        INF = float("inf")
        total_value = sum(self.values)
        for i_polygon, __ in enumerate(self.polygons):
            n_points_exp = int(
                round(
                    self.total_value * self.values[i_polygon] / total_value, 0
                )
            )

            k_to_n = p_to_k_to_n[i_polygon]

            for __ in range(n_points_exp):
                row = []
                for k in sorted_ks:
                    cost = INF
                    if k in k_to_n:
                        cost = 1.0 / k_to_n[k]
                    row.append(cost)
                cost_matrix.append(row)
        return cost_matrix

    def get_p_to_k_to_n_and_sorted_ks(self, dim):
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
        return p_to_k_to_n, sorted_ks

    def get_points_list(self, optimal_assignment, sorted_ks, total_value, dim):
        points_list = []
        ij_to_ik = dict(optimal_assignment)
        k_set = set()
        ij = 0
        for i_polygon in range(len(self.polygons)):
            n_points_exp = int(
                round(
                    self.total_value * self.values[i_polygon] / total_value, 0
                )
            )
            points = []
            for __ in range(n_points_exp):
                ik = ij_to_ik[ij]
                ij += 1
                k = sorted_ks[ik]
                if k in k_set:
                    log.error(f"Duplicate k: {k}")
                k_set.add(k)
                points.append(Point(k))
            points_list.append(points)

        points_list = HexBin.normalize(points_list, dim)
        return points_list

    def get_idx(self, points_list):
        idx = dict(
            zip(
                self.labels,
                [
                    sorted(
                        [list(point.coords[0]) for point in points],
                        key=lambda x: (x[1], x[0]),
                    )
                    for points in points_list
                ],
            )
        )
        return idx

    def get_group_type_to_group_to_points(self, idx):
        group_type_to_group_to_points = {}
        for group_type in self.group_label_to_group.keys():
            group_to_points = {}
            for label, points in idx.items():
                group = self.group_label_to_group[group_type][label]
                if group not in group_to_points:
                    group_to_points[group] = []
                group_to_points[group].extend(points)
            group_type_to_group_to_points[group_type] = group_to_points
        return group_type_to_group_to_points

    @staticmethod
    def get_idx2(group_type_to_group_to_points):
        idx2 = {}
        for (
            group_type,
            group_to_points,
        ) in group_type_to_group_to_points.items():
            idx2[group_type] = {}
            for group, points in group_to_points.items():
                polygons = HexBin.get_group_polygons(
                    [
                        Point(point[0], point[1] / HexBin.X_TO_Y_RATIO)
                        for point in points
                    ],
                    1,
                )
                idx2[group_type][group] = [
                    [
                        (point[0], point[1] * HexBin.X_TO_Y_RATIO)
                        for point in polygon.exterior.coords
                    ]
                    for polygon in polygons
                ]
        return idx2

    def build(
        self,
    ):
        total_area = sum([polygon.area for polygon in self.polygons])
        dim = (
            math.sqrt(total_area)
            * HexBin.SCALE_FACTOR
            / math.sqrt(self.total_value)
        )

        p_to_k_to_n, sorted_ks = self.get_p_to_k_to_n_and_sorted_ks(dim)
        cost_matrix = self.get_cost_matrix(p_to_k_to_n, sorted_ks)
        optimal_assignment = Hungarian(cost_matrix).run()
        points_list = self.get_points_list(
            optimal_assignment, sorted_ks, self.total_value, dim
        )
        idx = self.get_idx(points_list)
        if self.post_process:
            idx = self.post_process(dict(idx=idx))["idx"]

        group_type_to_group_to_points = self.get_group_type_to_group_to_points(
            idx
        )
        idx2 = HexBin.get_idx2(group_type_to_group_to_points)

        return dict(
            idx=idx,
            idx2=idx2,
            dim=1,
        )

    @staticmethod
    def validate(data):
        idx = data["idx"]
        duplicate_idx = {}
        for label, points in idx.items():
            for point in points:
                point = tuple(point)
                if point in duplicate_idx:
                    log.error(
                        f"{point}: '{label}'"
                        + f" Duplicated with {duplicate_idx[point]}"
                    )
                if point not in duplicate_idx:
                    duplicate_idx[point] = []
                duplicate_idx[point].append(label)

    def write(self, hexbin_data_path):
        data = self.build()
        self.validate(data)
        JSONFile(hexbin_data_path).write(data)
        log.info(f"Wrote {hexbin_data_path}")
