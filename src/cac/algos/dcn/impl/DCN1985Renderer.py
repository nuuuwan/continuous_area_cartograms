import math

import geopandas
from matplotlib import colors as mcolors
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
    def get_color(hue, log2_error):
        saturation = 100

        # lightness
        max_abs_error = 1
        p_log2_error = (
            min(max_abs_error, max(-max_abs_error, log2_error))
            + max_abs_error
        ) / (max_abs_error * 2)
        min_lightness = 20
        lightness = min_lightness + (100 - min_lightness) * p_log2_error

        r, g, b = mcolors.hsv_to_rgb(
            [hue / 360, saturation / 100, lightness / 100]
        )
        return (r, g, b)

    @staticmethod
    def render_polygon_shape(polygon, hue, log2_error):
        gdf = geopandas.GeoDataFrame(geometry=[polygon])
        gdf.plot(
            ax=plt.gca(),
            facecolor=DCN1985Renderer.get_color(hue, log2_error),
            edgecolor="white",
            linewidth=0.2,
        )

    def render_polygon_text(
        self,
        polygon,
        label,
        end_value,
        log2_error,
        show_start_labels,
        hue,
    ):
        background_color = DCN1985Renderer.get_color(hue, log2_error)
        foreground_color = DCN1985Renderer.get_foreground_color(
            background_color
        )
        x, y = polygon.centroid.coords[0]
        p_area = polygon.area / self.total_area
        BASE_FONT_SIZE = 12
        font_size = BASE_FONT_SIZE * math.sqrt(p_area)
        if font_size < 1:
            return
        if show_start_labels:
            number_label = ''
        else:
            number_label = Number(end_value).humanized()

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

    def render_polygon(
        self,
        polygon,
        label,
        end_value,
        log2_error,
        show_start_labels,
        hue,
    ):
        DCN1985Renderer.render_polygon_shape(polygon, hue, log2_error)
        self.render_polygon_text(
            polygon,
            label,
            end_value,
            log2_error,
            show_start_labels,
            hue,
        )

    def render_titles(self, show_start_labels):
        plt.annotate(
            self.render_params.title,
            (0.5, 0.95),
            fontsize=5,
            xycoords='axes fraction',
            ha='center',
        )
        if show_start_labels:
            title_text = self.render_params.start_value_unit
        else:
            title_text = self.render_params.end_value_unit

        plt.annotate(
            title_text,
            (0.5, 0.88),
            fontsize=10,
            xycoords='axes fraction',
            ha='center',
        )

    def render_all(self):
        plt.close()
        max_error = 10
        p_progress = (
            max_error - min(max_error, self.mean_abs_log2_error)
        ) / max_error
        log.debug(
            f'mean_abs_log2_error={self.mean_abs_log2_error}, {p_progress=}'
        )
        show_start_labels = p_progress < 0.1
        hue = (
            p_progress * self.render_params.end_value_hue
            + (1 - p_progress) * self.render_params.start_value_hue
        )
        log.debug(
            f'start_value_hue={self.render_params.start_value_hue}, end_value_hue={self.render_params.end_value_hue}, {hue=}'
        )

        for polygon, label, end_value, log2_error in zip(
            self.polygons,
            self.labels,
            self.values,
            self.Log2Error,
        ):
            self.render_polygon(
                polygon,
                label,
                end_value,
                log2_error,
                show_start_labels,
                hue,
            )

        DCN1985Renderer.remove_grids()
        self.render_titles(show_start_labels)

    def save_image(self, image_path, i_iter):
        self.render_all()
        plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
        log.info(f'Wrote {image_path}')
