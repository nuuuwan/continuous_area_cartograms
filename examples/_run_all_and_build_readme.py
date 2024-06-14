import os
import sys

from utils import File, Log

log = Log('build_readme_examples')
DIR_EXAMPLES = 'examples'


def run_system(cmd):
    log.info(f'🤖 {cmd}')
    os.system(cmd)


URL_RAW_BASE = (
    'https://raw.githubusercontent.com'
    + '/nuuuwan/continuous_area_cartograms'
    + '/main/examples'
)
URL_BASE = (
    'https://github.com'
    + '/nuuuwan/continuous_area_cartograms'
    + '/tree/main/examples'
)


def render_animated_gif(dir_name):
    url_animated_gif = URL_RAW_BASE + '/' + dir_name + '/output/animated.gif'
    url_example = URL_BASE + '/' + dir_name

    md_lines = [
        '',
        f'  <a href="{url_example}">',
        f'    <img src="{url_animated_gif}" height="320px" />',
        '  </a>',
        '',
    ]
    return md_lines


def get_dir_names():
    dir_names = []
    for dir_name in os.listdir(DIR_EXAMPLES):
        if os.path.isdir(os.path.join(DIR_EXAMPLES, dir_name)):
            dir_names.append(dir_name)
    return dir_names


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


def get_readme_lines_for_example(
    dir_name,
):
    dir_path = os.path.join(DIR_EXAMPLES, dir_name)
    dir_path_unix = dir_path.replace('\\', '/')
    os.path.join(dir_path, 'output')

    label = dir_name.replace('_', ' ').title()
    md_lines = (
        [
            f'### [{label}]({dir_path_unix})',
            '',
            '<p align="center">',
        ]
        + render_animated_gif(dir_name)
        + [
            '</p>',
            '',
        ]
    )

    md_lines.extend(build_code(dir_path))

    md_path = os.path.join(DIR_EXAMPLES, dir_name, 'README.md')
    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')

    run_system(f'git add "{md_path}')
    run_system(
        'git commit -m ' + f'"🤖 [_run_all_and_build_readme.py] {md_path}"'
    )

    return md_lines


def build_readme(dir_names):
    md_lines = [
        '# Examples',
        '',
    ]
    for dir_name in dir_names:
        md_lines.extend(get_readme_lines_for_example(dir_name))

    md_path = os.path.join(DIR_EXAMPLES, 'README.md')
    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')

    run_system(f'git add "{md_path}')
    run_system(
        'git commit -m ' + f'"🤖 [_run_all_and_build_readme.py] {md_path}"'
    )


def build_example_gallery(dir_names):
    md_lines = [
        '# Example Gallery',
        '',
        '<p align="center">',
    ]

    for dir_name in dir_names:
        md_lines.extend(render_animated_gif(dir_name))

    md_lines.extend(
        [
            '</p>',
            '',
        ]
    )

    md_path = os.path.join('README.example_gallery.md')
    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')

    run_system(f'git add "{md_path}')
    run_system(
        'git commit -m ' + f'"🤖 [_run_all_and_build_readme.py] {md_path}"'
    )


def run_all(dir_names, force_build):
    for dir_name in dir_names:
        output_path = os.path.join(DIR_EXAMPLES, dir_name, 'output')
        if not force_build and os.path.exists(output_path):
            log.warning(f'Output exists for {dir_name}. Skipping...')
            continue

        py_path = os.path.join(DIR_EXAMPLES, dir_name, 'source.py')
        py_cmd = f'python {py_path}'
        run_system(py_cmd)
        run_system(f'git add "examples/{dir_name}"')
        run_system(
            'git commit -m '
            + f'"🤖 [_run_all_and_build_readme.py] {dir_name}"'
        )


def process_all(force_build):
    dir_names = get_dir_names()
    build_example_gallery(dir_names)
    build_readme(dir_names)
    run_all(dir_names, force_build)


if __name__ == "__main__":
    force_build = len(sys.argv) > 1 and sys.argv[1] == 'force_build'
    process_all(force_build)
