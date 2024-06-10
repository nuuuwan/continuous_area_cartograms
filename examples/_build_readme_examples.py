import os

from utils import File, Log

log = Log('build_readme_examples')


def main():
    md_lines = [
        '# Examples',
        '',
    ]
    for file_name in os.listdir('examples'):
        if not file_name.startswith('example_'):
            continue
        file_path = os.path.join('examples', file_name)
        log.debug(f'Processing {file_path}')
        file_path_unix = file_path.replace('\\', '/')
        py_lines = File(file_path).read_lines()

        dir_output = os.path.join(
            'example_images',
            file_name[:-3],
        )
        animated_gif_path = os.path.join(dir_output, 'animated.gif')

        md_lines.extend(
            [
                f'## [{file_name}]({file_path_unix})',
                '',
                f'![{file_path}]({animated_gif_path})',
                '',
                '```python',
            ]
        )
        md_lines.extend(py_lines[1:-4])
        md_lines.extend(['```', ''])

    md_path = 'README.examples.md'
    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')


if __name__ == "__main__":
    main()
