import sys

from utils import Log

from cac import Example

log = Log('build_readme_examples')
DIR_EXAMPLES = 'examples'


def process_all(force_build):
    for example in Example.list():
        example.run(force_build)
        example.build_markdown()


if __name__ == "__main__":
    force_build = len(sys.argv) > 1 and sys.argv[1] == 'force_build'
    process_all(force_build)
