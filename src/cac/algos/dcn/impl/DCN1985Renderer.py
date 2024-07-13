import math

import geopandas
from matplotlib import colors as mcolors
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from utils import Log

from utils_future import MatPlotLibUser, Number

log = Log('DCN1985Renderer')


FONT_PATH = (
    "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\Windows\\Fonts\\p22.ttf"
)
FONT = FontProperties(fname=FONT_PATH)
plt.rcParams['font.family'] = FONT.get_name()


class DCN1985Renderer(MatPlotLibUser):
    HEIGHT = 4.5
    @staticmethod
    def get_foreground_color(background_color):
        r, g, b, alpha = mcolors.to_rgba(background_color)

        def blend(x):
            return x * alpha + 255 * (1 - alpha)

        [blended_r, blended_g, blended_b] = [blend(x) for x in [r, g, b]]

        luminance = 0.299 * blended_r + 0.587 * blended_g + 0.114 * blended_b

        if luminance < 0.5:
            return 'white'
        return 'black'

    @staticmethod
    def get_color(color, log2_error):
        r, g, b, alpha = mcolors.to_rgba(color)

        max_abs_error = 2
        p_log2_error = (
            min(max_abs_error, max(-max_abs_error, log2_error))
            + max_abs_error
        ) / (max_abs_error * 2)
        MIN_ALPHA = 0.1
        alpha2 = MIN_ALPHA + (1 - p_log2_error) * (1 - MIN_ALPHA)
        final_alpha = max(MIN_ALPHA, alpha * alpha2)
        return (r, g, b, final_alpha)

    @staticmethod
    def render_polygon_shape(polygon, color, log2_error):
        background_color = DCN1985Renderer.get_color(color, log2_error)
        foreground_color = DCN1985Renderer.get_foreground_color(
            background_color
        )
        gdf = geopandas.GeoDataFrame(geometry=[polygon])
        gdf.plot(
            ax=plt.gca(),
            facecolor=background_color,
            edgecolor="gray" if foreground_color == 'black' else 'white',
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
            fontsize=base_font_size,
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
            (0.5, 0.9 - 0.2),
            fontsize=base_font_size,
            xycoords='figure fraction',
            ha='center',
        )

        plt.annotate(
            self.render_params.footer_text,
            (0.5, 0.1),
            fontsize=base_font_size,
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

    def save_image(self, image_path, i_iter):
        plt.close()
        height = self.HEIGHT
        width = self.aspect_ratio * height
        plt.gcf().set_size_inches(width, height)
        
        # TESTING
        show_start_labels = i_iter <= -1
        
        self.render_all(show_start_labels)
        
        plt.savefig(image_path, dpi=150, pad_inches=0)
        log.info(f'Wrote {image_path}')
