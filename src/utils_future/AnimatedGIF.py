import os

import imageio.v2 as iio2
import imageio.v3 as iio3
from utils import Log

log = Log('AnimatedGIF')


class AnimatedGIF:
    def __init__(self, animated_gif_path, duration=200):
        self.animated_gif_path = animated_gif_path
        self.duration = duration

    def write(self, image_path_list):
        with iio2.get_writer(
            self.animated_gif_path, mode='I', duration=self.duration
        ) as writer:
            for image_path in image_path_list:
                image = iio3.imread(image_path)
                writer.append_data(image)
            n = len(image_path_list)
            log.info(f'Wrote {n} images to {self.animated_gif_path}')


if __name__ == "__main__":
    n = 10
    dir_path = os.path.join('images', 'ents.provinces')
    image_path_list = [
        os.path.join(dir_path, f'{i}.png') for i in range(0, n + 1)
    ]
    animated_gif_path = os.path.join(dir_path, 'animated.gif')
    AnimatedGIF(animated_gif_path).write(image_path_list)
