import math

import geopandas
from matplotlib import colors as mcolors
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from utils import Log

from utils_future import MatPlotLibUser, Number

log = Log('DCN1985Renderer')


class DCN1985Renderer(MatPlotLibUser):
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
    def render_polygon_shape(polygon, log2_error):
        gdf = geopandas.GeoDataFrame(geometry=[polygon])
        gdf.plot(
            ax=plt.gca(),
            facecolor=DCN1985Renderer.get_color(log2_error),
            edgecolor="white",
            linewidth=0.2,
        )

    @staticmethod
    def render_polygon_text(
        polygon,
        label,
        actual_value,
        log2_error,
        total_area,
        is_area_mode,
        true_total_area,
    ):
        background_color = DCN1985Renderer.get_color(log2_error)
        foreground_color = DCN1985Renderer.get_foreground_color(
            background_color
        )
        x, y = polygon.centroid.coords[0]
        p_area = polygon.area / total_area
        BASE_FONT_SIZE = 12
        font_size = BASE_FONT_SIZE * math.sqrt(p_area)
        if font_size < 1:
            return
        if is_area_mode:
            actual_area = p_area * true_total_area
            number_label = Number(actual_area).humanized()
        else:
            number_label = Number(actual_value).humanized()

        text = f'{label}\n{number_label}'

        plt.text(
            x,
            y,
            text,
            color=foreground_color,
            fontsize=font_size,
            horizontalalignment='center',
            verticalalignment='center',
        )

    @staticmethod
    def render_polygon(
        polygon,
        label,
        actual_value,
        log2_error,
        total_area,
        is_area_mode,
        true_total_area,
    ):
        DCN1985Renderer.render_polygon_shape(polygon, log2_error)
        DCN1985Renderer.render_polygon_text(
            polygon,
            label,
            actual_value,
            log2_error,
            total_area,
            is_area_mode,
            true_total_area,
        )

    @staticmethod
    def render_legend():
        handles = []
        for log2_error in [-1, -0.5, -0.25, 0, 0.25, 0.5, 1]:
            label = f'{2**log2_error:.0%}'
            background_color = DCN1985Renderer.get_color(log2_error)
            patch = mpatches.Patch(color=background_color, label=label)
            handles.append(patch)
        plt.gca().legend(
            handles=handles, fontsize=3, loc="best", frameon=False
        )

    def render_titles(self, is_area_mode):
        plt.annotate(
            self.render_params.title,
            (0.5, 0.95),
            fontsize=5,
            xycoords='axes fraction',
            ha='center',
        )
        if is_area_mode:
            title_text = f'By Area ({self.render_params.area_unit})'
        else:
            title_text = 'By ' + self.render_params.value_unit

        plt.annotate(
            title_text,
            (0.5, 0.88),
            fontsize=10,
            xycoords='axes fraction',
            ha='center',
        )

    def render_all(self, is_area_mode):
        plt.close()
        total_area = self.total_area
        for polygon, label, actual_value, log2_error in zip(
            self.polygons,
            self.labels,
            self.ActualValue,
            self.Log2Error,
        ):
            DCN1985Renderer.render_polygon(
                polygon,
                label,
                actual_value,
                log2_error,
                total_area,
                is_area_mode,
                self.render_params.true_total_area,
            )
        DCN1985Renderer.render_legend()
        DCN1985Renderer.remove_grids()
        self.render_titles(is_area_mode)

    def save_image(self, image_path, i_iter):
        self.render_all(i_iter < self.algo_params.max_iterations / 10)
        plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
        log.info(f'Wrote {image_path}')
