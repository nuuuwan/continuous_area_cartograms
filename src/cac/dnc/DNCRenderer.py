import topojson
from matplotlib import colors as mcolors
from matplotlib import pyplot as plt
from utils import Log

from utils_future import Number

log = Log('DNCRenderer')


class DNCRenderer:
    @staticmethod
    def get_foreground_color(background_color):
        rgba = mcolors.to_rgba(background_color)
        luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
        if luminance < 0.5:
            return 'white'
        return 'black'

    @staticmethod
    def get_color(log2_error):
        log2_error = max(min(log2_error, 1), -1)
        p = (log2_error + 1) / 2
        r, g, b = [int(c * 255) for c in plt.cm.jet(p)[:3]]
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def render_polygon_shape(grouped_polygon, ax):
        shapely_polygon = grouped_polygon.shapely_polygon
        log2_error = grouped_polygon.log2_error
        gdf = topojson.Topology(shapely_polygon).to_gdf()
        background_color = DNCRenderer.get_color(log2_error)
        gdf.plot(
            ax=ax,
            facecolor=background_color,
            edgecolor="white",
            linewidth=0.1,
        )

    @staticmethod
    def render_polygon_text(grouped_polygon):
        log2_error = grouped_polygon.log2_error
        shapely_polygon = grouped_polygon.shapely_polygon
        background_color = DNCRenderer.get_color(log2_error)

        foreground_color = DNCRenderer.get_foreground_color(background_color)
        x, y = shapely_polygon.centroid.coords[0]
        actual = grouped_polygon.actual
        plt.text(
            x,
            y,
            Number(actual).humanized(),
            color=foreground_color,
            fontsize=3,
            horizontalalignment='center',
            verticalalignment='center',
        )

    @staticmethod
    def render_polygon(grouped_polygon, ax):
        DNCRenderer.render_polygon_shape(grouped_polygon, ax)
        DNCRenderer.render_polygon_text(grouped_polygon)

    @staticmethod
    def remove_grids(ax):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

    @staticmethod
    def render_all(
        grouped_polygons,
    ):
        plt.close()
        ax = plt.gca()
        for grouped_polygon in grouped_polygons:
            DNCRenderer.render_polygon(grouped_polygon, ax)
        DNCRenderer.remove_grids(ax)

    @staticmethod
    def save_image(grouped_polygons, image_path):
        DNCRenderer.render_all(grouped_polygons)
        plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
        log.info(f'Wrote {image_path}')
