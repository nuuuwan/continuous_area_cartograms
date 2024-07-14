import os
import shutil
import tempfile

from PIL import ImageDraw
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

    def build_cell(self, job_id: str, i: int, j: int):
        path_id = f'{job_id}.{i}.{j}'
        dcn = self.dcn_list_list[i][j]

        dir_path_cell = os.path.join(tempfile.gettempdir(), path_id)
        shutil.rmtree(dir_path_cell, ignore_errors=True)
        os.makedirs(dir_path_cell)

        dcn.render_params.super_title = ''
        dcn.render_params.footer_text = ''
        dcn.build(dir_path_cell)

        dir_image_path = os.path.join(dir_path_cell, 'images')
        image_path_list_for_row_original = [
            os.path.join(dir_image_path, file_name)
            for file_name in os.listdir(dir_image_path)
        ]

        image_path_list_for_cell = []
        for k in range(self.FRAMES_PER_STAGE):
            m = int(
                k
                * len(image_path_list_for_row_original)
                / self.FRAMES_PER_STAGE
            )
            image_path_list_for_cell.append(
                image_path_list_for_row_original[m]
            )
        return image_path_list_for_cell

    def build_row_combined_frame(
        self, i, job_id, image_path_list_for_i, k, super_title, footer_text
    ):
        combined_im, total_width, height = self.combine_images(
            image_path_list_for_i, k
        )

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
            tempfile.gettempdir(), f'{job_id}.combined.{i}.{k}.png'
        )
        combined_im.save(combined_image_path)
        log.debug(f'Combined image saved to {combined_image_path}')
        return combined_image_path

    def build_row_combined_frames(
        self, i, job_id, image_path_list_for_i, super_title, footer_text
    ):
        combined_image_path_list_for_row = []
        for k in range(self.FRAMES_PER_STAGE):
            combined_image_path = self.build_row_combined_frame(
                i, job_id, image_path_list_for_i, k, super_title, footer_text
            )
            combined_image_path_list_for_row.append(combined_image_path)

        return combined_image_path_list_for_row

    def build_row(self, dir_path, i):
        dcn_list = self.dcn_list_list[i]
        job_id = os.path.basename(dir_path)

        image_path_list_for_i = []
        for j in range(len(dcn_list)):
            image_path_list_for_cell = self.build_cell(job_id, i, j)
            image_path_list_for_i.append(image_path_list_for_cell)

        super_title = dcn_list[0].render_params.super_title
        footer_text = dcn_list[0].render_params.footer_text

        return self.build_row_combined_frames(
            i, job_id, image_path_list_for_i, super_title, footer_text
        )

    def build_final_animated_gif(
        self, dir_path: str, combined_image_path_list: list[str]
    ):
        animated_gif_path = os.path.join(dir_path, 'animated.gif')
        AnimatedGIF(
            animated_gif_path,
            total_duration_s=self.DURATION_PER_STAGE * len(self),
        ).write_from_image_path_list(combined_image_path_list)

    def build(self, dir_path: str):
        combined_image_path_list = []
        for i in range(len(self)):
            combined_image_path_list_for_row = self.build_row(dir_path, i)
            combined_image_path_list.extend(combined_image_path_list_for_row)
            combined_image_path_list.extend(
                combined_image_path_list_for_row[::-1]
            )

        self.build_final_animated_gif(dir_path, combined_image_path_list)
