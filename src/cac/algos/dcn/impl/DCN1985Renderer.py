import math
from functools import cached_property

import geopandas
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from utils import Log

from utils_future import Color, MatPlotLibUser, Number

log = Log('DCN1985Renderer')


FONT_PATH = (
    "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\Windows\\Fonts\\p22.ttf"
)
FONT = FontProperties(fname=FONT_PATH)
plt.rcParams['font.family'] = FONT.get_name()


class DCN1985Renderer(MatPlotLibUser):
    HEIGHT = 4.5

    @staticmethod
    def get_color(color, log2_error):
        MAX_ABS_ERROR = 2
        p_log2_error = (
            min(MAX_ABS_ERROR, max(-MAX_ABS_ERROR, log2_error))
            + MAX_ABS_ERROR
        ) / (MAX_ABS_ERROR * 2)
        return Color(color).get_p(p_log2_error)

    @staticmethod
    def render_polygon_shape(polygon, color, log2_error):
        background_color = DCN1985Renderer.get_color(color, log2_error)
        foreground_color = background_color.foreground
        gdf = geopandas.GeoDataFrame(geometry=[polygon])
        gdf.plot(
            ax=plt.gca(),
            facecolor=background_color.rgba,
            edgecolor="#ccc" if foreground_color.x == 'black' else 'white',
            linewidth=0.2,
        )

    def render_polygon_text(
        self,
        polygon,
        label,
        end_value,
        log2_error,
        show_start_labels,
        color,
    ):
        background_color = DCN1985Renderer.get_color(color, log2_error)
        foreground_color = background_color.foreground
        x, y = polygon.centroid.coords[0]
        p_area = polygon.area / self.total_area
        BASE_FONT_SIZE = 12
        font_size = BASE_FONT_SIZE * math.sqrt(p_area) * self.render_scale
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
            color=foreground_color.rgba,
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
        color,
    ):
        DCN1985Renderer.render_polygon_shape(polygon, color, log2_error)
        self.render_polygon_text(
            polygon,
            label,
            end_value,
            log2_error,
            show_start_labels,
            color,
        )

    def render_titles(self, show_start_labels):
        base_font_size = 5

        plt.annotate(
            self.render_params.super_title,
            (0.5, 0.9),
            fontsize=base_font_size * 2,
            xycoords='figure fraction',
            ha='center',
        )

        title = '' if show_start_labels else self.render_params.title
        plt.annotate(
            title,
            (0.5, 0.9 - 0.05),
            fontsize=base_font_size * 3,
            xycoords='figure fraction',
            ha='center',
        )

        plt.annotate(
            self.render_params.sub_title,
            (0.5, 0.9 - 0.08),
            fontsize=base_font_size * 1.5,
            xycoords='figure fraction',
            ha='center',
        )

        plt.annotate(
            self.render_params.footer_text,
            (0.5, 0.1),
            fontsize=base_font_size * 2,
            xycoords='figure fraction',
            ha='center',
        )

    def render_all(self, show_start_labels: bool):
        color = (
            self.render_params.start_value_color
            if show_start_labels
            else self.render_params.end_value_color
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
                color,
            )

        DCN1985Renderer.remove_grids()
        self.render_titles(show_start_labels)

    @cached_property
    def render_scale(self) -> float:
        BASE_SCALE = 0.7
        return math.sqrt(self.render_params.scale) * BASE_SCALE

    def save_image(self, image_path, i_iter, width_prev=None):
        plt.close()
        height = self.HEIGHT
        width = width_prev or int(self.aspect_ratio * height ) 
        
        fig = plt.gcf()
        fig.set_size_inches(width, height)
        left = 0.5 - self.render_scale / 2
        right = 0.5 + self.render_scale / 2
        bottom = left
        top = right
        fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)

        show_start_labels = i_iter == 0

        self.render_all(show_start_labels)

        plt.savefig(image_path, dpi=150, pad_inches=0)
        log.info(f'Wrote {image_path}')
        return width
