import os

from utils import File, Log

log = Log('build_readme_examples')


def build_single(file_name, show_code):
    log.debug(f'Processing {file_name}')
    file_path = os.path.join('examples', file_name)
    file_path_unix = file_path.replace('\\', '/')

    dir_output = os.path.join(
        'example_images',
        file_name[:-3],
    )
    animated_gif_path = os.path.join(dir_output, 'animated.gif')

    md_lines = [
        f'### [{file_name}]({file_path_unix})',
        '',
        f'![{file_path}]({animated_gif_path})',
        '',
    ]

    if show_code:
        py_lines = File(file_path).read_lines()
        md_lines.extend(
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


def build_all(show_code, md_path):
    md_lines = [
        '# Continuous Area Cartogram - Examples',
        '',
        '## Examples',
        '',
    ]
    for file_name in os.listdir('examples'):
        if not file_name.startswith('example_'):
            continue
        md_lines.extend(build_single(file_name, show_code))

    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')


if __name__ == "__main__":
    build_all(True, 'README.example.long.md')
    build_all(False, 'README.example.short.md')
