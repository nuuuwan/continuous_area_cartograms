import math
import os

from shapely import MultiPolygon, Point, Polygon
from shapely.ops import unary_union
from utils import JSONFile, Log, _

from cac.extended.HexBin import HexBin

log = Log("HexBinRenderer")


class HexBinRenderer:
    SCALE_FACTOR = 1
    N_POLYGON_SIDES = 6

    def __init__(self, polygons, labels, label_to_group, colors, values, total_value):
        self.polygons = polygons
        self.labels = labels
        self.label_to_group = label_to_group
        self.colors = colors
        self.values = values
        self.total_value = total_value

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
    def render_group(points, dim):
        polygons = []
        for point in points:
            polygons.append(
                HexBinRenderer.get_polygon(point, dim, expand_factor=1.01)
            )
        combined = unary_union(polygons)

        polygons = []
        if isinstance(combined, Polygon):
            polygons = [combined]
        elif not isinstance(combined, MultiPolygon):
            polygons = list(combined.geoms)
        else:
            polygons = []

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
                    stroke='#eee',
                    stroke_width=dim * 0.05,
                ),
            )
            rendered_polygons.append(rendered_polygon)
        return _('g', rendered_polygons)

    @staticmethod
    def render_label(label, point, dim):
        inner = []
        words = label.split(' ')
        font_size = 1.5 * dim / max([len(word) for word in words])
        n = len(words)
        for i, word in enumerate(words):
            inner.append( _(
                'text',
                word,
                dict(
                    x=point.x,
                    y=point.y + font_size * (i - (n - 1)/2),
                    fill="black",
                    font_size=font_size,
                    font_family="P22 Johnston Underground Regular",
                    text_anchor="middle",
                    dominant_baseline="middle",
                ),
            ))
        return _('g', inner)

    @staticmethod
    def render_point(point, dim, color, label):
        polygon = HexBinRenderer.get_polygon(point, dim)
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
                        stroke="#ccc",
                        stroke_width=dim * 0.01,
                    ),
                ),
                HexBinRenderer.render_label(label, point, dim),
            ],
        )

    def render(self, points_list, dim):
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

        min_x -= dim * 2
        min_y -= dim * 2
        max_x += dim * 2
        max_y += dim * 2
        x_span = max_x - min_x
        y_span = max_y - min_y

        rendered_points = []
        rendered_groups = []

        group_to_points = {}
        for i_polygon, [points, color, label] in enumerate(
            zip(points_list, self.colors, self.labels)
        ):
            if len(points) == 0:
                log.error(f'{i_polygon}) {label} - No points.')
            for point in points:
                rendered_points.append(
                    HexBinRenderer.render_point(point, dim, color, label)
                )

            group = self.label_to_group[label]
            if group not in group_to_points:
                group_to_points[group] = []
            group_to_points[group].extend(points)

        for group, points in group_to_points.items():
            rendered_groups.append(HexBinRenderer.render_group(points, dim))

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
            + rendered_points
            + rendered_groups,
            dict(
                height=500,
                width=300,
                viewBox=f"{min_x} {min_y} {x_span} {y_span}",
            ),
        )

    def save_hexbin(self, hexbin_path):
        hexbin_data_path = hexbin_path + '.json'
        # if not os.path.exists(hexbin_data_path):
        HexBin(self.polygons, self.values, self.total_value, self.labels).write(hexbin_data_path)
        data = JSONFile(hexbin_data_path).read()
        dim = data['dim']

        points_list = [
            [
                Point(point[0], point[1] / HexBin.X_TO_Y_RATIO)
                for point in points
            ]
            for points in data['idx'].values()
        ]
        svg = self.render(points_list, dim)

        svg.store(hexbin_path)
        log.info(f"Wrote {hexbin_path}")
        os.startfile(hexbin_path)