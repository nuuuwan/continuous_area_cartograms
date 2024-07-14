from PIL import Image, ImageFont

FONT_PATH = (
    "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\Windows\\Fonts\\p22.ttf"
)


class PillowUser:
    @staticmethod
    def get_font(font_size: int) -> ImageFont:
        return ImageFont.truetype(FONT_PATH, font_size)

    @staticmethod
    def combine_images(image_path_list_for_i: list[str], k) -> Image:
        im_list = []
        for image_path_list in image_path_list_for_i:
            im = Image.open(image_path_list[k])
            im_list.append(im)

        total_width = sum(im.width for im in im_list)
        height = max(im.height for im in im_list)
        combined_im = Image.new('RGB', (total_width, height))

        x_offset = 0
        for im in im_list:
            combined_im.paste(im, (x_offset, 0))
            x_offset += im.width
        return combined_im, total_width, height
