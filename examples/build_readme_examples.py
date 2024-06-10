import os   
from utils import Log, File

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

        md_lines.extend([f'## [{file_name}]({file_path_unix})', '','```python'])
        md_lines.extend(py_lines[1:-4])
        md_lines.extend(['```', ''])

    md_path = 'README.examples.md'
    File(md_path).write_lines(md_lines)
    log.info(f'Wrote {md_path}')
if __name__ == "__main__":
    main()