import os

from utils import File, Log

from utils_future import Markdown

log = Log('Example')


class Example:
    URL_RAW_BASE = "/".join(
        [
            'https://raw.githubusercontent.com',
            'nuuuwan/continuous_area_cartograms',
            'main/examples',
        ]
    )

    def __init__(self, example_name):
        self.example_name = example_name

    @staticmethod
    def list():
        examples = []
        for example_name in os.listdir('examples'):
            if os.path.isdir(os.path.join('examples', example_name)):
                example = Example(example_name)
                examples.append(example)
        return examples

    @property
    def dir_path(self):
        return os.path.join(
            'examples',
            self.example_name,
        )

    @property
    def title(self):
        return self.example_name.replace('_', ' ').title()

    # Code & Output
    @property
    def py_path(self):
        return os.path.join(
            self.dir_path,
            '__main__.py',
        )

    @property
    def has_output(self):
        return os.path.exists(
            os.path.join(self.dir_path, 'output')
        ) and os.path.exists(self.animated_gif_path)

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
            self.dir_path,
            
            'animated.gif',
        )

    @property
    def url_animated_gif(self):
        return (
            Example.URL_RAW_BASE
            + '/'
            + self.example_name
            + '/output/animated.gif'
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
            self.dir_path,
            'README.md',
        )

    def build_markdown(self):
        self.markdown.save(self.readme_path)
        log.info(f'Wrote {self.readme_path}')
