import math
import os

import topojson
from matplotlib import patches
from matplotlib import pyplot as plt
from shapely import affinity
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.ops import unary_union
from utils import Log

from utils_future import MatPlotLibUser

log = Log("HexBin")


class HexBin(MatPlotLibUser):
    SCALE_FACTOR = 1

    def __init__(self, polygons, labels, total_value):
        self.polygons = polygons
        self.labels = labels
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
    def get_hexagon_centroids_for_polygon(polygon, dim, points_set):
        polygon = HexBin.get_scaled_polygon(polygon)
        minx, miny, maxx, maxy = polygon.bounds
        dimx = dim
        dimy = dim / math.cos(math.pi / 6)

        x_min = int(minx / dimx) * dimx
        y_min = int(miny / dimy) * dimy
        points = []
        x = x_min
        while x <= maxx:
            y = y_min
            ix = int(x / dimx)
            if ix % 2 == 0:
                y += dimy / 4
            else:
                y -= dimy / 4

            while y <= maxy:
                point = Point(x, y)

                if point not in points_set:
                    if polygon.contains(point):
                        points.append(point)

                y += dimy
            x += dimx

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
                    facecolor="none",
                    edgecolor="black",
                    linewidth=2,
                )
            )

    @staticmethod
    def render_region_polygons(dim, points, label, ax, color):
        inner_polygons = []
        for point in points:
            polygon_points = []
            r = (dim / math.cos(math.pi / 6) ** 2) / 2
            N_POLYGON_SIDES = 6
            for i in range(N_POLYGON_SIDES):
                angle = 2 * math.pi / N_POLYGON_SIDES * i
                x = point.x + r * math.cos(angle)
                y = point.y + r * math.sin(angle)
                polygon_points.append((x, y))

            polygon_patch = patches.Polygon(
                polygon_points,
                facecolor=color,
                edgecolor=color,
                alpha=0.5,
            )
            ax.add_patch(polygon_patch)
            inner_polygons.append(Polygon(polygon_points))

            # add label
            ax.text(
                point.x,
                point.y,
                label,
                fontsize=dim * 20,
                ha="center",
                va="center",
            )

        HexBin.render_region_border(ax, inner_polygons)

    def save_hexbin(self, hexbin_path):
        width = 10
        height = int(width * 1.5)
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)

        polygons = self.polygons

        total_area = sum([polygon.area for polygon in self.polygons])
        dim = round(math.sqrt(total_area / self.total_value) * HexBin.SCALE_FACTOR, 3)

        for polygon in polygons:
            HexBin.render_polygon_shape(polygon, ax)

        n_polygons = len(polygons)

        points_set = set()
        for i_polygon, polygon in enumerate(polygons):
            points = HexBin.get_hexagon_centroids_for_polygon(polygon, dim, points_set)

            actual_n_points = len(points)
            expected_n_points = int(
                round(self.total_value * polygon.area / total_area, 0)
            )
            emoji = ""
            if actual_n_points < expected_n_points:
                emoji = "🔵"
            elif actual_n_points > expected_n_points:
                emoji = "🔴"
            label = self.labels[i_polygon]
            log.debug(
                f"{label}".ljust(15)
                + f"{emoji} {actual_n_points}/{expected_n_points}".rjust(10)
            )

            points_set |= set(points)
            color = plt.cm.hsv((i_polygon * 199 % n_polygons) / n_polygons)

            HexBin.render_region_polygons(dim, points, label, ax, color)

        self.remove_grids()

        plt.savefig(hexbin_path)
        log.info(f"Wrote {hexbin_path}")
        os.startfile(hexbin_path)
