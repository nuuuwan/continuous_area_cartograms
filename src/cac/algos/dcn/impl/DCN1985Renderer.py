import math
import os
import tempfile
from functools import cached_property

import geopandas
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from utils import Hash

from utils_future import Color, Log, MatPlotLibUser, Number

log = Log("DCN1985Renderer")


class DCN1985Renderer(MatPlotLibUser):
    RENDER_VERSION = "20241028-1144"
    HEIGHT = 4.5
    BASE_SCALE = 0.8
    DPI = 240
    BASE_FONT_SIZE = 10

    @property
    def image_hash(self):
        data = dict(
            polygons=self.polygons,
            values=self.values,
            labels=self.labels,
            render_params=str(self.render_params),
            params=[
                self.HEIGHT,
                self.BASE_SCALE,
                self.DPI,
                self.BASE_FONT_SIZE,
            ],
            version=self.RENDER_VERSION,
        )
        return Hash.md5(str(data))

    @staticmethod
    def get_color(color, log2_error):
        MAX_ABS_ERROR = 2
        p_log2_error = (
            min(MAX_ABS_ERROR, max(-MAX_ABS_ERROR, log2_error)) + MAX_ABS_ERROR
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
            edgecolor="#ccc" if foreground_color.x == "black" else "white",
            linewidth=0.2,
        )

    def render_polygon_text(
        self,
        polygon,
        label,
        end_value,
        log2_error,
        color,
    ):
        background_color = DCN1985Renderer.get_color(color, log2_error)
        foreground_color = background_color.foreground
        x, y = polygon.centroid.coords[0]
        p_area = polygon.area / self.total_area
        font_size = 2 * (
            self.BASE_FONT_SIZE * math.sqrt(p_area) * self.render_scale
        )
        if font_size < 1:
            return
        number_label = Number(end_value).humanized()

        text = f"{label}\n{number_label}"

        plt.text(
            x,
            y,
            text,
            color=foreground_color.rgba,
            fontsize=font_size,
            horizontalalignment="center",
            verticalalignment="center",
        )

    def render_polygon(
        self,
        polygon,
        label,
        end_value,
        log2_error,
        color,
    ):
        DCN1985Renderer.render_polygon_shape(polygon, color, log2_error)
        self.render_polygon_text(
            polygon,
            label,
            end_value,
            log2_error,
            color,
        )

    def render_titles(self):
        # Header
        plt.annotate(
            self.render_params.super_title,
            (0.5, 0.95),
            fontsize=self.BASE_FONT_SIZE,
            xycoords="figure fraction",
            ha="center",
            color="gray",
        )
        title = self.render_params.title
        plt.annotate(
            title,
            (0.5, 0.9 - 0.0275),
            fontsize=self.BASE_FONT_SIZE * 2.5,
            xycoords="figure fraction",
            ha="center",
        )
        plt.annotate(
            self.render_params.sub_title,
            (0.5, 0.9 - 0.09),
            fontsize=self.BASE_FONT_SIZE,
            xycoords="figure fraction",
            ha="center",
            color="gray",
        )
        plt.annotate(
            self.render_params.footer_text,
            (0.5, 0.1),
            fontsize=self.BASE_FONT_SIZE,
            xycoords="figure fraction",
            ha="center",
        )

    def render_all(self):
        color = self.render_params.end_value_color

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
                color,
            )

        DCN1985Renderer.remove_grids()
        self.render_titles()

    @cached_property
    def render_scale(self) -> float:
        return math.sqrt(self.render_params.scale) * self.BASE_SCALE

    def save_image(self, width_prev=None):
        image_path = os.path.join(
            tempfile.gettempdir(), f"cac.dcn.{self.image_hash}.png"
        )
        if os.path.exists(image_path):
            return image_path, width_prev

        plt.close()
        height = self.HEIGHT
        width = width_prev or round(self.aspect_ratio * height, 1)

        fig = plt.gcf()
        fig.set_size_inches(width, height)
        left = 0.5 - self.render_scale / 2
        right = 0.5 + self.render_scale / 2
        bottom = left
        top = right
        fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom)

        self.render_all()

        plt.savefig(image_path, dpi=self.DPI, pad_inches=0)
        log.debug(f"Wrote {image_path}")
        return image_path, width
