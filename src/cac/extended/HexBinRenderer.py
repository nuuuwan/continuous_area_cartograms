import os

from shapely import Point, Polygon
from utils import JSONFile, Log, _

from cac.extended.HexBin import HexBin
from utils_future import Color

log = Log("HexBinRenderer")


class STYLE:
    FONT_FAMILY = "sans-serif"


def convert_to_superscript(n):
    s = str(f"{n:.0f}").strip()
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[int(c)] for c in s])


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
        custom_color_map=None,
        rendered_svg_custom=None,
    ):
        self.polygons = polygons
        self.labels = labels
        self.group_to_label_to_group = group_to_label_to_group
        self.colors = colors
        self.values = values
        self.total_value = total_value
        self.custom_color_map = custom_color_map or {}
        self.rendered_svg_custom = rendered_svg_custom or []

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
                    stroke_width=dim * (0.1 + 0.07 * (i_group)),
                    opacity=0.5,
                ),
            )
            rendered_polygons.append(rendered_polygon)
        return _("g", rendered_polygons)

    @staticmethod
    def render_label(label, point, dim, text_color):
        inner = []

        font_size = 0.1 * dim

        inner.append(
            _(
                "text",
                label,
                dict(
                    x=point.x,
                    y=point.y + font_size * 0.1,
                    fill="#000",
                    font_size=font_size,
                    font_family=STYLE.FONT_FAMILY,
                    text_anchor="middle",
                    dominant_baseline="middle",
                ),
            )
        )
        inner.append(
            _(
                "text",
                f"{point.x:.1f},{point.y * HexBin.X_TO_Y_RATIO:.1f}",
                dict(
                    x=point.x,
                    y=point.y + font_size * 1.4,
                    fill="#000",
                    font_size=font_size * 2,
                    font_family=STYLE.FONT_FAMILY,
                    text_anchor="middle",
                    dominant_baseline="middle",
                ),
            )
        )
        return _("g", inner)

    @staticmethod
    def render_point(
        point,
        dim,
        color,
        label,
        text_color,
    ):
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
                        stroke="#333",
                        stroke_width=dim * 0.02,
                    ),
                ),
                HexBinRenderer.render_label(label, point, dim, text_color),
            ],
        )

    @staticmethod
    def render_grid_polygon(polygon, dim):
        return _(
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
        )

    @staticmethod
    def render_grid_text(x, y, dim, dim_x, dim_y):
        return _(
            "text",
            f"{x / dim_x:.1f},{y / dim_y:.1f}",
            dict(
                x=x,
                y=y,
                fill="#ccc",
                font_size=dim * 0.3,
                text_anchor="middle",
                dominant_baseline="middle",
            ),
        )

    @staticmethod
    def render_grid(min_x, min_y, max_x, max_y, dim):
        dim_x = dim
        dim_y = dim / HexBin.X_TO_Y_RATIO
        inner = []
        x = min_x
        while True:
            y = min_y + dim_y / 2
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

    @staticmethod
    def get_midpoint_i(points_list):
        # get mean point
        x, y = 0, 0
        for point in points_list:
            x += point.x
            y += point.y
        x /= len(points_list)
        y /= len(points_list)

        # find point closest to the mean point
        i_mid = None
        d_min = None
        for i_point, point in enumerate(points_list):
            d = (point.x - x) ** 2 + (point.y - y) ** 2
            if i_point == 0 or d < d_min:
                i_mid = i_point
                d_min = d
        return i_mid

    def get_rendered_points(self, points_list, dim):

        rendered_points = []

        for i_points, points in enumerate(points_list):

            label = self.labels[i_points]
            color = self.colors[i_points]
            i_mid = HexBinRenderer.get_midpoint_i(points)

            value = self.values[i_points]
            label_display_points = label + convert_to_superscript(value)

            for i_point, point in enumerate(points):
                label_display = ""
                if i_point == i_mid:
                    label_display = label_display_points
                # label_display = f"{label}{i+1}"

                point_color = (
                    self.custom_color_map.get((label, i_point + 1)) or color
                )

                text_color = Color(point_color).foreground.hex

                rendered_points.append(
                    HexBinRenderer.render_point(
                        point, dim, point_color, label_display, text_color
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
        PADDING = 1.7
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
        min_x, min_y, __, __, x_span, y_span = self.get_bbox_padded(
            points_list, dim
        )

        view_box = f"{min_x} {min_y} {x_span} {y_span}"
        log.debug(f"{view_box=}")
        mid_x = min_x + x_span / 2
        mid_y = min_y + y_span / 2
        log.debug(f"{mid_x=}, {mid_y=}")

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
                        fill="#fff",
                        stroke="#000",
                    ),
                )
            ]
            + rendered_points
            + rendered_groups
            + self.rendered_svg_custom,
            dict(
                height=3200,
                width=1800,
                viewBox=view_box,
                font_family=STYLE.FONT_FAMILY,
            ),
        )

    def write_data(self, hexbin_path, post_process=None):
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

    def write(self, hexbin_path, post_process=None):
        hexbin_data_path = self.write_data(hexbin_path, post_process)

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
        os.startfile(hexbin_path)
