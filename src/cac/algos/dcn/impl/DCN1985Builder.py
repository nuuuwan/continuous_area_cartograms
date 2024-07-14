import os
import shutil
import tempfile

from utils import Log

from utils_future import AnimatedGIF

log = Log('DCN1985Builder')


class DCN1985Builder:
    @staticmethod
    def get_dir_output_temp(dir_output):
        id = os.path.basename(dir_output)
        dir_output_temp = os.path.join(
            tempfile.gettempdir(),
            id,
        )
        shutil.rmtree(dir_output_temp, ignore_errors=True)
        os.makedirs(dir_output_temp)
        return dir_output_temp

    @staticmethod
    def save_image_helper(i_iter, dcn, dir_output_temp, width_prev):
        dir_image = os.path.join(dir_output_temp, 'images')
        if not os.path.exists(dir_image):
            os.makedirs(dir_image)
        file_id = f'{i_iter:03}'
        image_path = os.path.join(dir_image, f'{file_id}.png')
        width = dcn.save_image(image_path, i_iter, width_prev)
        return width


    @staticmethod
    def save_animated_gif(dir_output, dir_output_temp):
        dir_image = os.path.join(dir_output_temp, 'images')
        animated_gif_path = os.path.join(dir_output, 'animated.gif')
        AnimatedGIF(animated_gif_path).write_from_dir_path(dir_image)

    def build(self, dir_output=None, save_geojson=False):
        dir_output = dir_output or tempfile.mkdtemp()
        assert os.path.exists(dir_output)
        dcn_list = self.run_all(self)

        dir_output_temp = DCN1985Builder.get_dir_output_temp(dir_output)
        width_prev = None
        for i_iter, dcn in enumerate(dcn_list):
            width_prev = DCN1985Builder.save_image_helper(
                i_iter, dcn, dir_output_temp, width_prev
            )

        DCN1985Builder.save_animated_gif(dir_output, dir_output_temp)
