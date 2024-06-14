import math

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
    def render_polygon_shape(polygon, log2_error, ax):
        gdf = topojson.Topology(polygon).to_gdf()
        background_color = DNCRenderer.get_color(log2_error)
        gdf.plot(
            ax=ax,
            facecolor=background_color,
            edgecolor="white",
            linewidth=0.5,
        )

    @staticmethod
    def render_polygon_text(polygon, actual_value, log2_error, total_area):
        background_color = DNCRenderer.get_color(log2_error)
        foreground_color = DNCRenderer.get_foreground_color(background_color)
        x, y = polygon.centroid.coords[0]
        p_area = polygon.area / total_area
        BASE_FONT_SIZE = 15
        font_size = BASE_FONT_SIZE * math.sqrt(p_area)
        plt.text(
            x,
            y,
            Number(actual_value).humanized(),
            color=foreground_color,
            fontsize=font_size,
            horizontalalignment='center',
            verticalalignment='center',
        )

    @staticmethod
    def render_polygon(polygon, actual_value, log2_error, total_area, ax):
        DNCRenderer.render_polygon_shape(polygon, log2_error, ax)
        DNCRenderer.render_polygon_text(
            polygon, actual_value, log2_error, total_area
        )

    @staticmethod
    def remove_grids(ax):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

    @staticmethod
    def render_all(
        polygons,
        ActualValue,
        Log2Error,
    ):
        plt.close()
        ax = plt.gca()
        total_area = sum([polygon.area for polygon in polygons])
        for polygon, actual_value, log2_error in zip(
            polygons, ActualValue, Log2Error
        ):
            DNCRenderer.render_polygon(
                polygon, actual_value, log2_error, total_area, ax
            )
        DNCRenderer.remove_grids(ax)

    @staticmethod
    def _save_image(polygons, ActualValue, Log2Error, image_path):
        DNCRenderer.render_all(polygons, ActualValue, Log2Error)
        plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
        log.info(f'Wrote {image_path}')

    def save_image(self, image_path):
        DNCRenderer._save_image(
            self.polygons,
            self.ActualValue,
            self.Log2Error,
            image_path,
        )
        return image_path
