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

        for i, dcn in enumerate(self.dcn_list, start=1):
            log.debug(f'Running Stage {i}/{len(self)}')

            dir_path_stage = os.path.join(dir_path, f'stage_{i}')
            os.makedirs(dir_path_stage)

            dcn.run(dir_path_stage)

        # building animation
        image_path_list = []
        FRAMES_PER_STAGE = 20
        for i in range(1, len(self) + 1):
            dir_path_stage_images = os.path.join(
                dir_path, f'stage_{i}', 'images'
            )
            image_path_list_for_stage_original = []
            for file_name in os.listdir(dir_path_stage_images):
                image_path_list_for_stage_original.append(
                    os.path.join(dir_path_stage_images, file_name)
                )
            image_path_list_for_stage = []
            for i in range(FRAMES_PER_STAGE):
                j = int(
                    i
                    * len(image_path_list_for_stage_original)
                    / FRAMES_PER_STAGE
                )
                image_path_list_for_stage.append(
                    image_path_list_for_stage_original[j]
                )
            image_path_list.extend(image_path_list_for_stage)
            image_path_list.extend(image_path_list_for_stage[::-1])

        animated_gif_path = os.path.join(dir_path, 'animated.gif')
        DURATION_PER_STAGE = 10
        AnimatedGIF(
            animated_gif_path, total_duration_s=DURATION_PER_STAGE * len(self)
        ).write_from_image_path_list(image_path_list)
