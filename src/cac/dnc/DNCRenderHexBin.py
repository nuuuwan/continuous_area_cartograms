import math

import topojson
from matplotlib import patches
from matplotlib import pyplot as plt
from shapely import affinity
from shapely.geometry import Point
from utils import Log

log = Log('DNCRenderHexBin')


class DNCRenderHexBin:
    SCALE_FACTOR = 1

    @staticmethod
    def get_points(polygon, dim):
        polygon = affinity.scale(
            polygon,
            xfact=DNCRenderHexBin.SCALE_FACTOR,
            yfact=DNCRenderHexBin.SCALE_FACTOR,
            origin=polygon.centroid,
        )
        bounds = polygon.bounds
        minx, miny, maxx, maxy = bounds

        x_min = int(minx / dim) * dim
        y_min = int(miny / dim) * dim

        points = []
        x = x_min
        while x <= maxx:
            y = y_min
            ix = int(round(x / dim, 0))

            if ix % 2 == 1:
                y += dim / 2

            while y <= maxy:
                point = Point(x, y)
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

    def save_hexbin(self, hexbin_path):
        width = 10
        height = int(width * 1.4)
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)

        polygons = self.polygons

        total_area = sum([polygon.area for polygon in self.polygons])
        total_value = 220
        dim = (
            math.sqrt(total_area / total_value) * DNCRenderHexBin.SCALE_FACTOR
        )
        log.debug(f'{total_value=:,}, {dim=:4f}')

        for polygon in polygons:
            DNCRenderHexBin.render_polygon_shape(polygon, ax)

        n_polygons = len(polygons)
        actual_total_value = 0
        for i_polygon, polygon in enumerate(polygons):
            points = DNCRenderHexBin.get_points(polygon, dim)
            color = plt.cm.hsv(i_polygon / n_polygons)
            for point in points:
                polygon_patch = patches.RegularPolygon(
                    (point.x, point.y),
                    numVertices=6,
                    radius=dim / 2,
                    orientation=math.pi / 2,
                    facecolor=color,
                    edgecolor="#000",
                    alpha=0.25,
                )
                ax.add_patch(polygon_patch)

            actual_total_value += len(points)
        log.debug(f'{actual_total_value=:,}')

        self.remove_grids(ax)

        plt.savefig(hexbin_path)
        log.info(f'Wrote {hexbin_path}')

        # import sys
        # sys.exit(-1)
