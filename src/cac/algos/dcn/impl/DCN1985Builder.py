import os
import tempfile

from utils import Log

from utils_future import AnimatedGIF

log = Log('DCN1985Builder')


class DCN1985Builder:
    @staticmethod
    def save_animated_gif(dir_output, image_path_list):
        animated_gif_path = os.path.join(dir_output, 'animated.gif')
        AnimatedGIF(animated_gif_path).write_from_image_path_list(
            image_path_list
        )
        
    def build(
        self, dir_output=None, do_build_animated_gif=True, verbose=False
    ):
        dir_output = dir_output or tempfile.mkdtemp()
        assert os.path.exists(dir_output)
        dcn_list = self.run_all(self, verbose)

        width_prev = None
        image_path_list = []
        for dcn in dcn_list:
            image_path, width_prev = dcn.save_image(width_prev)
            image_path_list.append(image_path)

        if do_build_animated_gif:
            DCN1985Builder.save_animated_gif(dir_output, image_path_list)
        return image_path_list, dcn_list
