import math

import topojson
from matplotlib import pyplot as plt
from shapely.geometry import Point as ShapelyPoint
from utils import Log

log = Log('DNCRenderHexBin')


class DNCRenderHexBin:
    @staticmethod
    def get_points(shapely_polygon, n):
        minx, miny, maxx, maxy = shapely_polygon.bounds
        polygon_area = shapely_polygon.area
        dim = math.sqrt(polygon_area / n)

        points = []
        x = minx + dim / 2
        while x <= maxx - dim / 2:
            y = miny + dim / 2
            while y <= maxy - dim / 2:
                random_point = ShapelyPoint(x, y)
                if shapely_polygon.contains(random_point):
                    points.append(random_point)
                    if len(points) == n:
                        break
                y += dim
            if len(points) == n:
                break
            x += dim

        log.debug(f'{n}, {len(points)}')
        return points

    def save_hexbin(self, hexbin_path):
        width = 10
        height = int(width * 4 / 3)
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)
        x, y = [], []
        for shapely_polygon, value in zip(self.shapely_polygons, self.values):
            n = int(round(value / 100_000, 0))
            points = DNCRenderHexBin.get_points(shapely_polygon, n)
            x += [point.x for point in points]
            y += [point.y for point in points]
            gdf = topojson.Topology(shapely_polygon).to_gdf()
            gdf.plot(
                ax=ax,
                facecolor='#fff',
                edgecolor="#000",
                linewidth=1,
            )

        grid_m = 2
        hb = plt.hexbin(
            x,
            y,
            gridsize=(width * grid_m, height * grid_m),
            cmap='Blues',
            alpha=0.8,
        )
        fig.colorbar(hb, ax=ax)
        self.remove_grids(ax)

        plt.savefig(hexbin_path)
        log.info(f'Wrote {hexbin_path}')
