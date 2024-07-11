import os

import imageio.v2 as iio2
import imageio.v3 as iio3
from utils import Log

log = Log('AnimatedGIF')


class AnimatedGIF:
    def __init__(self, animated_gif_path, total_duration_s=10, loop=0):
        self.animated_gif_path = animated_gif_path
        self.total_duration_s = total_duration_s
        self.loop = loop

    def write(self, x):
        if isinstance(x, str):
            if not os.path.isdir(x):
                raise ValueError(f'{x} is not a directory')
            return self.write_from_dir_path(x)

        if not isinstance(x, list):
            raise ValueError(f'{x} is not a list')
        return self.write_from_image_path_list(x)

    def write_from_dir_path(self, dir_path):
        image_path_list = sorted(
            [os.path.join(dir_path, f) for f in os.listdir(dir_path)]
        )
        self.write_from_image_path_list(image_path_list)

    def write_from_image_path_list(self, image_path_list):
        image_path_list2 = image_path_list + image_path_list[::-1]
        n = len(image_path_list2)
        duration_ms = 1_000 * self.total_duration_s / n
        with iio2.get_writer(
            self.animated_gif_path,
            mode='I',
            duration=duration_ms,
            loop=self.loop,
        ) as writer:
            for image_path in image_path_list2:
                image = iio3.imread(image_path)
                writer.append_data(image)
            log.info(f'Wrote {n} images to {self.animated_gif_path}')


if __name__ == "__main__":
    n = 10
    dir_path = os.path.join('images', 'ents.province')
    image_path_list = [
        os.path.join(dir_path, f'{i}.png') for i in range(0, n + 1)
    ]
    animated_gif_path = os.path.join(dir_path, 'animated.gif')
    AnimatedGIF(animated_gif_path).write(image_path_list)
