import os
import shutil
import tempfile

from utils import Log

from cac.algos import DCN1985
from utils_future import AnimatedGIF

log = Log('MultiStageCAC')


class MultiStageCAC:
    def __init__(self, *dcn_list: list[DCN1985]):
        self.dcn_list = dcn_list

    def __len__(self):
        return len(self.dcn_list)

    def build_stages(self, path_id_prefix: str):
        for i, dcn in enumerate(self.dcn_list, start=1):
            log.debug(f'Running Stage {i}/{len(self)}')
            path_id = f'{path_id_prefix}.{i}'
            dir_path_stage = os.path.join(tempfile.gettempdir(), path_id)
            shutil.rmtree(dir_path_stage, ignore_errors=True)
            os.makedirs(dir_path_stage)

            dcn.run(dir_path_stage)

    def build_final_animation(
        self, dir_path: str, path_id_prefix: str, cac_id: str
    ):
        # building animation
        image_path_list = []
        FRAMES_PER_STAGE = 20
        for i in range(1, len(self) + 1):
            path_id = f'{path_id_prefix}.{i}'
            dir_path_stage_images = os.path.join(
                tempfile.gettempdir(), path_id, 'images'
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

        copy_animated_gif_path = os.path.join(
            os.environ['DIR_DESKTOP'],
            f'{cac_id}.animated.gif',
        )
        shutil.copyfile(animated_gif_path, copy_animated_gif_path)
        log.debug(f'Wrote {copy_animated_gif_path}')
        os.startfile(copy_animated_gif_path)

    def build(self, dir_path: str):
        cac_id = os.path.split(dir_path)[-1]
        path_id_prefix = f'cac.{cac_id}.stage'
        self.build_stages(path_id_prefix)
        self.build_final_animation(dir_path, path_id_prefix, cac_id)
