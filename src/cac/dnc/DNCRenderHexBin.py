from matplotlib import pyplot as plt
from utils import Log

log = Log('DNCRenderHexBin')


class DNCRenderHexBin:
    def save_hexbin(self, hexbin_path):
        plt.close()

        centroids = [
            shapely_polygon.centroid
            for shapely_polygon in self.shapely_polygons
        ]
        x = [point.x for point in centroids]
        y = [point.y for point in centroids]

        plt.hexbin(x, y, gridsize=10, cmap='Blues')

        self.remove_grids(plt.gca())

        plt.savefig(hexbin_path)
        log.info(f'Wrote {hexbin_path}')
