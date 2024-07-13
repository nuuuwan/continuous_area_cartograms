import os
import shutil
import tempfile

from PIL import Image, ImageDraw
from utils import Log

from cac.algos import DCN1985
from utils_future import AnimatedGIF, PillowUser

log = Log('GridCAC')


class GridCAC(PillowUser):
    FRAMES_PER_STAGE = 20
    DURATION_PER_STAGE = 10

    def __init__(self, dcn_list_list: list[list[DCN1985]]):
        self.dcn_list_list = dcn_list_list

    def __len__(self):
        return len(self.dcn_list_list)

    def build(self, dir_path: str):
        id = os.path.basename(dir_path)
        combined_image_path_list = []
        for i, dcn_list in enumerate(self.dcn_list_list):
            image_path_list_for_i = []
            super_title = dcn_list[0].render_params.super_title
            footer_text = dcn_list[0].render_params.footer_text
            for j, dcn in enumerate(dcn_list):
                path_id = f'{id}.{i}.{j}'
                dir_path_cell = os.path.join(tempfile.gettempdir(), path_id)
                shutil.rmtree(dir_path_cell, ignore_errors=True)
                os.makedirs(dir_path_cell)

                dcn.render_params.super_title = ''
                dcn.render_params.footer_text = ''
                dcn.run(dir_path_cell)

                dir_image_path = os.path.join(dir_path_cell, 'images')
                image_path_list_for_stage_original = [
                    os.path.join(dir_image_path, file_name)
                    for file_name in os.listdir(dir_image_path)
                ]

                image_path_list_for_stage_ij = []
                for k in range(self.FRAMES_PER_STAGE):
                    l = int(
                        k
                        * len(image_path_list_for_stage_original)
                        / self.FRAMES_PER_STAGE
                    )
                    image_path_list_for_stage_ij.append(
                        image_path_list_for_stage_original[l]
                    )
                image_path_list_for_i.append(image_path_list_for_stage_ij)

            combined_image_path_list_for_stage = []
            for k in range(self.FRAMES_PER_STAGE):
                im_list = []
                for j in range(len(dcn_list)):
                    im = Image.open(image_path_list_for_i[j][k])
                    im_list.append(im)

                total_width = sum(im.width for im in im_list)
                height = max(im.height for im in im_list)
                combined_im = Image.new('RGB', (total_width, height))

                x_offset = 0
                for im in im_list:
                    combined_im.paste(im, (x_offset, 0))
                    x_offset += im.width

                draw = ImageDraw.Draw(combined_im)
                draw.text(
                    (total_width / 2, 40),
                    super_title,
                    fill='black',
                    font=self.get_font(24),
                    anchor='ms',
                )
                draw.text(
                    (total_width / 2, height - 20),
                    footer_text,
                    fill='black',
                    font=self.get_font(12),
                    anchor='ms',
                )

                combined_image_path = os.path.join(
                    tempfile.gettempdir(), f'{id}.combined.{i}.{k}.png'
                )
                combined_im.save(combined_image_path)
                log.debug(f'Combined image saved to {combined_image_path}')
                combined_image_path_list_for_stage.append(combined_image_path)

            combined_image_path_list.extend(combined_image_path_list_for_stage)
            combined_image_path_list.extend(combined_image_path_list_for_stage[::-1])            
        animated_gif_path = os.path.join(dir_path, 'animated.gif')
        AnimatedGIF(
            animated_gif_path,
            total_duration_s=self.DURATION_PER_STAGE * len(self),
        ).write_from_image_path_list(combined_image_path_list)
