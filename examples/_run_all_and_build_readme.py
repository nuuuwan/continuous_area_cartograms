import os

from utils import File, Log

log = Log('build_readme_examples')
DIR_EXAMPLES = 'examples'


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

    md_lines.extend(build_code(dir_path))
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


def run_system(cmd):
    log.info(f'🤖 {cmd}')
    os.system(cmd)


def run_all(dir_names):
    for dir_name in dir_names:
        py_path = os.path.join(DIR_EXAMPLES, dir_name, 'source.py')
        py_cmd = f'python {py_path}'
        run_system(py_cmd)
        run_system(f'git add "examples/{dir_name}"')
        run_system(
            'git commit -m '
            + f'"🤖 [_run_all_and_build_readme.py] {dir_name}"'
        )
        break


def process_all():
    dir_names = get_dir_names()
    build_readme(dir_names)
    run_all(dir_names)


if __name__ == "__main__":
    process_all()
