import os

from shapely import Point, Polygon
from utils import JSONFile, Log, _

from cac.extended.HexBin import HexBin

log = Log("HexBinRenderer")


class HexBinRenderer:
    SCALE_FACTOR = 1
    N_POLYGON_SIDES = 6

    def __init__(
        self, polygons, labels, label_to_group, colors, values, total_value
    ):
        self.polygons = polygons
        self.labels = labels
        self.label_to_group = label_to_group
        self.colors = colors
        self.values = values
        self.total_value = total_value

    @staticmethod
    def render_group(polygons, dim):
        rendered_polygons = []
        for polygon in polygons:
            rendered_polygon = _(
                'polygon',
                None,
                dict(
                    points=' '.join(
                        [f'{x[0]},{x[1]}' for x in polygon.exterior.coords]
                    ),
                    fill=None,
                    stroke='#222',
                    stroke_width=dim * 0.1,
                ),
            )
            rendered_polygons.append(rendered_polygon)
        return _('g', rendered_polygons)

    @staticmethod
    def render_label(label, point, dim):
        inner = []
        words = label.split(' ')
        font_size = 1.5 * dim / max([len(word) for word in words] + [1])
        n = len(words)
        for i, word in enumerate(words):
            inner.append(
                _(
                    'text',
                    word,
                    dict(
                        x=point.x,
                        y=point.y + font_size * (i - (n - 1) / 2),
                        fill="black",
                        font_size=font_size,
                        font_family="P22 Johnston Underground Regular",
                        text_anchor="middle",
                        dominant_baseline="middle",
                    ),
                )
            )
        return _('g', inner)

    @staticmethod
    def render_point(point, dim, color, label):
        polygon = HexBin.get_polygon(point, dim)
        return _(
            'g',
            [
                _(
                    'polygon',
                    None,
                    dict(
                        points=' '.join(
                            [
                                f'{x[0]},{x[1]}'
                                for x in polygon.exterior.coords
                            ]
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
                        'g',
                        [
                            _(
                                'polygon',
                                None,
                                dict(
                                    points=' '.join(
                                        [
                                            f'{x[0]},{x[1]}'
                                            for x in polygon.exterior.coords
                                        ]
                                    ),
                                    fill=None,
                                    stroke="#ccc",
                                    stroke_width=dim * 0.01,
                                ),
                            ),
                            _(
                                'text',
                                f'{x / dim_x:.1f},{y / dim_y:.1f}',
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
                        ],
                    )
                )
                y += dim_y
                if y > max_y:
                    break

            x += dim_x
            if x > max_x:
                break

        return _('g', inner)

    def render(self, points_list, group_to_polygons, dim):
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
        PADDING = 1

        min_x -= dim_x * PADDING
        min_y -= dim_y * PADDING

        max_x += dim_x * PADDING
        max_y += dim_y * PADDING

        x_span = max_x - min_x
        y_span = max_y - min_y

        rendered_points = []
        for i, points in enumerate(points_list):
            color = self.colors[i]
            label = self.labels[i]
            for point in points:
                rendered_points.append(
                    HexBinRenderer.render_point(point, dim, color, label)
                )

        rendered_groups = []
        for group, polygons in group_to_polygons.items():
            rendered_groups.append(HexBinRenderer.render_group(polygons, dim))

        return _(
            'svg',
            [
                _(
                    'rect',
                    None,
                    dict(
                        x=min_x,
                        y=min_y,
                        width=x_span,
                        height=y_span,
                        fill='#8881',
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

    def save_hexbin(self, hexbin_path, post_process=None):
        hexbin_data_path = hexbin_path + '.json'
        HexBin(
            self.polygons,
            self.values,
            self.total_value,
            self.labels,
            self.label_to_group,
            post_process,
        ).write(hexbin_data_path)

        data = JSONFile(hexbin_data_path).read()

        dim = data['dim']
        points_list = [
            [
                Point(point[0], point[1] / HexBin.X_TO_Y_RATIO)
                for point in points
            ]
            for points in data['idx'].values()
        ]
        group_to_polygons = {
            k: [
                Polygon(
                    [[vii[0], vii[1] / HexBin.X_TO_Y_RATIO] for vii in vi]
                )
                for vi in v
            ]
            for k, v in data['idx2'].items()
        }

        svg = self.render(points_list, group_to_polygons, dim)

        svg.store(hexbin_path)
        log.info(f"Wrote {hexbin_path}")
        os.startfile(hexbin_path)
