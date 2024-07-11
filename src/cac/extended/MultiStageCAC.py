import os
import shutil

from utils import Log

from cac.algos import DCN1985
from utils_future import AnimatedGIF

log = Log('MultiStageCAC')


class MultiStageCAC:
    def __init__(self, *dcn_list: list[DCN1985]):
        self.dcn_list = dcn_list

    def __len__(self):
        return len(self.dcn_list)

    def run(self, dir_path: str = None):
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path)
        polygons = None
        for i, dcn in enumerate(self.dcn_list, start=1):
            log.debug(f'Running Stage {i}/{len(self)}')
            dcn_copy = dcn.from_dcn(polygons) if polygons else dcn

            dir_path_stage = os.path.join(dir_path, f'stage_{i}')
            os.makedirs(dir_path_stage)
            polygons = dcn_copy.run(dir_path_stage)

        # building animation
        image_path_list = []
        for i in range(1, len(self) + 1):
            dir_path_stage_images = os.path.join(
                dir_path, f'stage_{i}', 'images'
            )
            for file_name in os.listdir(dir_path_stage_images):
                image_path_list.append(
                    os.path.join(dir_path_stage_images, file_name)
                )

        animated_gif_path = os.path.join(dir_path, 'animated.gif')
        AnimatedGIF(animated_gif_path).write_from_image_path_list(
            image_path_list
        )
