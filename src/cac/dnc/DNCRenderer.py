from functools import cache

import topojson
from matplotlib import pyplot as plt
from utils import Log

log = Log('DNCRenderer')


class DNCRenderer:
    @staticmethod
    @cache
    def get_color(log2_error):
        log2_error = max(min(log2_error, 1), -1)
        p = (log2_error + 1) / 2
        r, g, b = [int(c * 255) for c in plt.cm.jet(p)[:3]]
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def save_image(grouped_polygons, image_path):
        plt.close()
        ax = plt.gca()
        for i, grouped_polygon in enumerate(grouped_polygons):
            shapely_polygon = grouped_polygon.shapely_polygon
            log2_error = grouped_polygon.log2_error
            gdf = topojson.Topology(shapely_polygon).to_gdf()
            gdf.plot(
                ax=ax,
                facecolor=DNCRenderer.get_color(log2_error),
                edgecolor="white",
                linewidth=0.1,
            )

        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
        log.info(f'Wrote {image_path}')
