import os

from utils import File, Log

from utils_future import Markdown

log = Log('Example')


class Example:
    URL_RAW_BASE = "/".join(
        [
            'https://raw.githubusercontent.com',
            'nuuuwan/continuous_area_cartograms',
            'main',
        ]
    )

    DIR_EXAMPLE_GROUP_PATH_LIST = [
        'examples_mcac',
        'examples',
    ]

    def __init__(self, dir_example_path):
        self.dir_example_path = dir_example_path

    @property
    def dir_example_path_unix(self) -> str:
        return self.dir_example_path.replace('\\', '/')

    @property
    def example_name(self):
        return os.path.basename(self.dir_example_path)

    @staticmethod
    def list():
        examples = []
        for dir_example_group_path in Example.DIR_EXAMPLE_GROUP_PATH_LIST:
            for child_dir_name in os.listdir(dir_example_group_path):
                dir_example_path = os.path.join(
                    dir_example_group_path, child_dir_name
                )

                if not os.path.isdir(dir_example_path):
                    continue
                example = Example(dir_example_path)
                examples.append(example)

        return examples

    @property
    def title(self):
        return self.example_name.replace('_', ' ').title()

    # Code & Output
    @property
    def py_path(self):
        return os.path.join(
            self.dir_example_path,
            '__main__.py',
        )

    @property
    def has_output(self):
        return os.path.exists(self.animated_gif_path)

    def run(self, force_build):
        if not force_build and self.has_output:
            log.debug(f'Skipping {self.example_name} (already built)')
            return

        py_cmd = f'python {self.py_path}'
        log.info(f'💻 {py_cmd}')
        os.system(py_cmd)

    # ReadMe
    @property
    def animated_gif_path(self):
        return os.path.join(
            self.dir_example_path,
            'animated.gif',
        )

    @property
    def url_animated_gif(self):
        return '/'.join(
            [
                Example.URL_RAW_BASE,
                self.dir_example_path_unix,
                'animated.gif',
            ]
        )

    @property
    def source_content(self):
        return File(self.py_path).read()

    @property
    def markdown(self):
        return Markdown.h1(
            Markdown(self.title),
            Markdown.p_html(
                Markdown.img_html(self.url_animated_gif),
                align='center',
            ),
            Markdown.code(
                'python',
                Markdown(self.source_content),
            ),
        )

    @property
    def readme_path(self):
        return os.path.join(
            self.dir_example_path,
            'README.md',
        )

    def build_markdown(self):
        self.markdown.save(self.readme_path)
        log.info(f'Wrote {self.readme_path}')
