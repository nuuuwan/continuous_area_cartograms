import os

from utils import File, Log

log = Log('build_readme_examples')
DIR_EXAMPLES = 'examples'


def build_code(dir_path):
    py_path = os.path.join(dir_path, 'source.py')
    py_lines = File(py_path).read_lines()
    md_lines = (
        [
            '```python',
        ]
        + py_lines[1:-4]
        + [
            '```',
        ]
    )

    md_lines.extend([''])
    return md_lines


def build_single(dir_name, show_code):
    log.debug(f'Processing {dir_name}')
    dir_path = os.path.join(DIR_EXAMPLES, dir_name)
    dir_path_unix = dir_path.replace('\\', '/')
    os.path.join(dir_path, 'output')
    animated_gif_path = os.path.join(
        dir_name, 'output', 'animated.gif'
    ).replace('\\', '/')

    label = dir_name.replace('_', ' ').title()
    md_lines = [
        f'### [{label}]({dir_path_unix})',
        '',
        '<p align="center">',
        f'  <img src="{animated_gif_path}" width="240px" />',
        '</p>',
        '',
    ]

    if show_code:
        md_lines.extend(build_code(dir_path))

    return md_lines


def build_all(show_code, md_path):
    md_lines = [
        '# Examples',
        '',
    ]
    for dir_name in os.listdir(DIR_EXAMPLES):
        if os.path.isdir(os.path.join(DIR_EXAMPLES, dir_name)):
            md_lines.extend(build_single(dir_name, show_code))

    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')


if __name__ == "__main__":
    build_all(True, os.path.join(DIR_EXAMPLES, 'README.md'))