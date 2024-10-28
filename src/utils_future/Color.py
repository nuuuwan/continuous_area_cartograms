import colorsys
import random
from functools import cache, cached_property

from matplotlib import colors as mcolors


class Color:
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(self.x)

    @cached_property
    def rgba(self) -> tuple:
        return mcolors.to_rgba(self.x)

    @cached_property
    def blended_rgb(self) -> tuple:
        r, g, b, a = self.rgba

        def blend(x):
            return x * a + 255 * (1 - a)

        [br, bg, bb] = [blend(x) for x in [r, g, b]]
        return (br, bg, bb)

    @cached_property
    def luminance(self) -> float:
        [br, bg, bb] = self.blended_rgb
        return 0.299 * br + 0.587 * bg + 0.114 * bb

    @cached_property
    def foreground(self) -> "Color":
        if self.luminance < 0.5:
            return Color("white")
        return Color("black")

    @cache
    def get_p(self, p) -> "Color":
        r, g, b, alpha = self.rgba
        MIN_ALPHA = 0.1
        alpha2 = MIN_ALPHA + (1 - p) * (1 - MIN_ALPHA)
        final_alpha = max(MIN_ALPHA, alpha * alpha2)
        return Color((r, g, b, final_alpha))

    @staticmethod
    def random(h=None, s=100, v=90, a=0.99) -> "Color":
        if h is None:
            h = random.randint(0, 360)
        r, g, b = mcolors.hsv_to_rgb((h / 360, s / 100, v / 100))
        hex = mcolors.to_hex((r, g, b, a))
        return hex

    @staticmethod
    def from_hls(hue, light, sat) -> "Color":
        r, g, b = colorsys.hls_to_rgb(hue / 360, light / 100, sat / 100)
        return Color((r, g, b))

    @cached_property
    def hex(self) -> str:
        return mcolors.to_hex(self.rgba)
