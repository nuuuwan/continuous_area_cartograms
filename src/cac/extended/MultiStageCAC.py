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
        start_value_unit = None
        start_total_value = None
        start_value_hue = None

        for i, dcn in enumerate(self.dcn_list, start=1):
            log.debug(f'Running Stage {i}/{len(self)}')

            render_params = dcn.render_params
            if start_value_unit:
                render_params.start_value_unit = start_value_unit
                render_params.start_total_value = start_total_value
                render_params.start_value_hue = start_value_hue

            dcn_copy = dcn.from_dcn(
                polygons=polygons, render_params=render_params
            )

            dir_path_stage = os.path.join(dir_path, f'stage_{i}')
            os.makedirs(dir_path_stage)

            polygons = dcn_copy.run(dir_path_stage)
            start_value_unit = dcn_copy.render_params.end_value_unit
            start_total_value = sum(dcn_copy.values)
            start_value_hue = dcn_copy.render_params.end_value_hue

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
        AnimatedGIF(animated_gif_path,total_duration_s=5 * len(self)).write_from_image_path_list(
            image_path_list
        )
