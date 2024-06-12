import os

from utils import File, Log

log = Log('build_readme_examples')


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
    dir_path = os.path.join('examples', dir_name)
    dir_path_unix = dir_path.replace('\\', '/')
    dir_output = os.path.join(dir_path, 'output')
    animated_gif_path = os.path.join(dir_output, 'animated.gif').replace(
        '\\', '/'
    )
    animated_hexbin_gif_path = os.path.join(dir_output, 'animated.hexbin.gif').replace(
        '\\', '/'
    )   

    label = dir_name.replace('_', ' ').title()
    md_lines = [
        f'### [{label}]({dir_path_unix})',
        '',
        f'![{label}]({animated_gif_path})',
        '',
         f'![{label}]({animated_hexbin_gif_path})',
        '',
    ]

    if show_code:
        md_lines.extend(build_code(dir_path))

    return md_lines


def build_all(show_code, md_path):
    md_lines = [
        '# Continuous Area Cartogram - Examples',
        '',
        '## Examples',
        '',
    ]
    for dir_name in os.listdir('examples'):
        if not os.path.isdir(os.path.join('examples', dir_name)):
            continue
        if not dir_name.startswith('example_'):
            continue
        md_lines.extend(build_single(dir_name, show_code))

    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')


if __name__ == "__main__":
    build_all(True, 'README.example.long.md')
    build_all(False, 'README.example.short.md')
