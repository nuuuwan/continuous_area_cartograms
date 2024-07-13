from PIL import ImageFont

FONT_PATH = (
    "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\Windows\\Fonts\\p22.ttf"
)


class PillowUser:
    @staticmethod
    def get_font(font_size: int) -> ImageFont:
        return ImageFont.truetype(FONT_PATH, font_size)
