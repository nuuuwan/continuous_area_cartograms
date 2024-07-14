import math

import topojson
from matplotlib import patches
from matplotlib import pyplot as plt
from shapely import affinity
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union
from utils import Log

from utils_future import MatPlotLibUser

log = Log('HexBin')


class HexBin(MatPlotLibUser):
    SCALE_FACTOR = 1

    def __init__(self, polygons, total_value=10):
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
    def get_points(polygon, dim, points_set):
        polygon = HexBin.get_scaled_polygon(polygon)
        minx, miny, maxx, maxy = polygon.bounds

        x_min, y_min = [int(x / dim) * dim for x in [minx, miny]]
        points = []
        x = x_min
        while x <= maxx:
            y = y_min
            ix = int(x / dim)
            if ix % 2 == 0:
                y += dim / 4
            else:
                y -= dim / 4

            while y <= maxy:
                point = Point(x, y)
  
                if point not in points_set:
                    if polygon.contains(point):
                        points.append(point)

                y += dim
            x += dim

        return points

    @staticmethod
    def render_polygon_shape(polygon, ax):
        gdf = topojson.Topology(polygon).to_gdf()
        gdf.plot(
            ax=ax,
            facecolor="#fff0",
            edgecolor="black",
            linewidth=0.1,
        )

    @staticmethod
    def render_region_border(ax, inner_polygons):
        combined_polygons = unary_union(inner_polygons)

        if isinstance(combined_polygons, Polygon):
            combined_polygons = [combined_polygons]
        elif isinstance(combined_polygons, MultiPolygon):
            combined_polygons = list(combined_polygons.geoms)
        else:
            combined_polygons = []

        for part_polygon in combined_polygons:
            ax.add_patch(
                patches.Polygon(
                    part_polygon.exterior.coords,
                    facecolor='none',
                    edgecolor='black',
                )
            )

    @staticmethod
    def render_region_polygons(dim, points, ax, color):
        inner_polygons = []
        for point in points:
            polygon_points = []
            r = 1.01 * math.sqrt(2) * dim / 2
            N_POLYGON_SIDES = 6
            for i in range(N_POLYGON_SIDES):
                angle = 2 * math.pi / N_POLYGON_SIDES * i
                x = point.x + r * math.cos(angle)
                y = point.y + r * math.sin(angle) * 0.9
                polygon_points.append((x, y))

            polygon_patch = patches.Polygon(
                polygon_points,
                facecolor=color,
                edgecolor=None,
                alpha=0.5,
            )
            ax.add_patch(polygon_patch)
            inner_polygons.append(Polygon(polygon_points))
        HexBin.render_region_border(ax, inner_polygons)

    def save_hexbin(self, hexbin_path):
        width = 10
        height = int(width * 1.4)
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)

        polygons = self.polygons

        total_area = sum([polygon.area for polygon in self.polygons])
        dim = round(
            math.sqrt(total_area / self.total_value) * HexBin.SCALE_FACTOR, 3
        )

        for polygon in polygons:
            HexBin.render_polygon_shape(polygon, ax)

        n_polygons = len(polygons)

        points_set = set()
        for i_polygon, polygon in enumerate(polygons):
            points = HexBin.get_points(polygon, dim, points_set)
            points_set |= set(points)
            color = plt.cm.hsv((i_polygon * 199 % n_polygons) / n_polygons)
            HexBin.render_region_polygons(dim, points, ax, color)

        self.remove_grids(ax)

        plt.savefig(hexbin_path)
        log.info(f'Wrote {hexbin_path}')
