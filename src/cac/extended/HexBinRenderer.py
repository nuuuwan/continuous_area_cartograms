from shapely import Point, Polygon
from utils import JSONFile, Log, _

from cac.extended.HexBin import HexBin

log = Log("HexBinRenderer")


def remove_vowels(x):
    if len(x) < 2:
        return x
    return x[0] + "".join([c for c in x[1:] if c.lower() not in "aeiou"])


def get_short_label(x):
    words = x.split(" ")
    if len(words) == 1:
        return remove_vowels(words[0])[:3].upper()
    return "".join([word[0] for word in words])


class HexBinRenderer:
    SCALE_FACTOR = 1
    N_POLYGON_SIDES = 6

    def __init__(
        self,
        polygons,
        labels,
        group_to_label_to_group,
        colors,
        values,
        total_value,
    ):
        self.polygons = polygons
        self.labels = labels
        self.group_to_label_to_group = group_to_label_to_group
        self.colors = colors
        self.values = values
        self.total_value = total_value

    @staticmethod
    def render_group(polygons, dim, i_group):
        rendered_polygons = []
        for polygon in polygons:
            rendered_polygon = _(
                "polygon",
                None,
                dict(
                    points=" ".join(
                        [f"{x[0]},{x[1]}" for x in polygon.exterior.coords]
                    ),
                    fill=None,
                    stroke="#222",
                    stroke_width=(1 + i_group) * dim * 0.07,
                    opacity=0.5 + 0.1 * i_group,
                ),
            )
            rendered_polygons.append(rendered_polygon)
        return _("g", rendered_polygons)

    @staticmethod
    def render_label(label, point, dim):
        inner = []

        short_label = label
        font_size = dim * 0.2

        inner.append(
            _(
                "text",
                short_label,
                dict(
                    x=point.x,
                    y=point.y,
                    fill="white",
                    font_size=font_size,
                    font_family="P22 Johnston Underground Regular",
                    text_anchor="middle",
                    dominant_baseline="middle",
                ),
            )
        )

        return _("g", inner)

    @staticmethod
    def render_point(point, dim, color, label):
        polygon = HexBin.get_polygon(point, dim)
        return _(
            "g",
            [
                _(
                    "polygon",
                    None,
                    dict(
                        points=" ".join(
                            [f"{x[0]},{x[1]}" for x in polygon.exterior.coords]
                        ),
                        fill=color,
                        stroke="#444",
                        stroke_width=dim * 0.01,
                    ),
                ),
                HexBinRenderer.render_label(label, point, dim),
            ],
        )

    @staticmethod
    def render_grid_polygon(polygon, dim):
        return (
            _(
                "polygon",
                None,
                dict(
                    points=" ".join(
                        [f"{x[0]},{x[1]}" for x in polygon.exterior.coords]
                    ),
                    fill=None,
                    stroke="#ccc",
                    stroke_width=dim * 0.01,
                ),
            ),
        )

    @staticmethod
    def render_grid_text(x, y, dim, dim_x, dim_y):
        return (
            _(
                "text",
                f"{x / dim_x:.1f},{y / dim_y:.1f}",
                dict(
                    x=x,
                    y=y,
                    fill="#ccc",
                    font_size=dim * 0.3,
                    font_family="P22 Johnston Underground Regular",
                    text_anchor="middle",
                    dominant_baseline="middle",
                ),
            ),
        )

    @staticmethod
    def render_grid(min_x, min_y, max_x, max_y, dim):
        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO
        inner = []
        x = min_x
        while True:
            y = min_y
            ix = int(round(x / dim_x))
            if ix % 2 == 0:
                y -= dim_y / 2
            while True:
                point = Point(x, y)
                polygon = HexBin.get_polygon(point, dim)
                inner.append(
                    _(
                        "g",
                        [
                            HexBinRenderer.render_grid_polygon(polygon, dim),
                            HexBinRenderer.render_grid_text(
                                x, y, dim, dim_x, dim_y
                            ),
                        ],
                    )
                )
                y += dim_y
                if y > max_y:
                    break
            x += dim_x
            if x > max_x:
                break
        return _("g", inner)

    def get_rendered_points(self, points_list, dim):

        rendered_points = []
        for i, points in enumerate(points_list):
            color = self.colors[i]
            label = self.labels[i]
            n = len(points)
            i_mid = (n - 1) // 2
            for i, point in enumerate(points):
                label_display = "" if i != i_mid else label
                rendered_points.append(
                    HexBinRenderer.render_point(
                        point, dim, color, label_display
                    )
                )
        return rendered_points

    def get_rendered_groups(self, group_type_to_group_to_polygons, dim):

        rendered_groups = []
        for i, group_to_polygons in enumerate(
            group_type_to_group_to_polygons.values()
        ):
            for polygons in group_to_polygons.values():
                rendered_groups.append(
                    HexBinRenderer.render_group(polygons, dim, i)
                )

        return rendered_groups

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
    def get_bbox_padded(points_list, dim):

        min_x, min_y, max_x, max_y = HexBinRenderer.get_bbox(points_list)

        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO
        PADDING = 1
        min_x -= dim_x * PADDING
        min_y -= dim_y * PADDING
        max_x += dim_x * PADDING
        max_y += dim_y * PADDING

        x_span = max_x - min_x
        y_span = max_y - min_y

        return min_x, min_y, max_x, max_y, x_span, y_span

    def render(self, points_list, group_type_to_group_to_polygons, dim):

        rendered_points = self.get_rendered_points(points_list, dim)
        rendered_groups = self.get_rendered_groups(
            group_type_to_group_to_polygons, dim
        )
        min_x, min_y, max_x, max_y, x_span, y_span = self.get_bbox_padded(
            points_list, dim
        )

        return _(
            "svg",
            [
                _(
                    "rect",
                    None,
                    dict(
                        x=min_x,
                        y=min_y,
                        width=x_span,
                        height=y_span,
                        fill="#8881",
                    ),
                )
            ]
            + [HexBinRenderer.render_grid(min_x, min_y, max_x, max_y, dim)]
            + rendered_points
            + rendered_groups,
            dict(
                height=500,
                width=300,
                viewBox=f"{min_x} {min_y} {x_span} {y_span}",
            ),
        )

    def save_hexbin_data(self, hexbin_path, post_process=None):
        hexbin_data_path = hexbin_path + ".json"
        HexBin(
            self.polygons,
            self.values,
            self.total_value,
            self.labels,
            self.group_to_label_to_group,
            post_process,
        ).write(hexbin_data_path)
        return hexbin_data_path

    def save_hexbin(self, hexbin_path, post_process=None):
        hexbin_data_path = self.save_hexbin_data(hexbin_path, post_process)

        data = JSONFile(hexbin_data_path).read()
        points_list = [
            [
                Point(point[0], point[1] / HexBin.X_TO_Y_RATIO)
                for point in points
            ]
            for points in data["idx"].values()
        ]
        group_type_to_group_to_polygons = {
            group_type: {
                group: [
                    Polygon(
                        [[vii[0], vii[1] / HexBin.X_TO_Y_RATIO] for vii in vi]
                    )
                    for vi in points
                ]
                for group, points in group_to_points.items()
            }
            for group_type, group_to_points in data["idx2"].items()
        }

        svg = self.render(
            points_list, group_type_to_group_to_polygons, data["dim"]
        )

        svg.store(hexbin_path)
        log.info(f"Wrote {hexbin_path}")
