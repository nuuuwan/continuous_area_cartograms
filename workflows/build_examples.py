import sys

from utils import File, Log

from cac import Example
from utils_future import Markdown

log = Log('build_readme_examples')
DIR_EXAMPLES = 'examples'


def build_readme():
    image_md_list = []
    for example in Example.list():
        image_md_list.append(Markdown.img_html(example.url_animated_gif,height="240px"))

    examples_md = Markdown.p_html(
        Markdown.concat(*image_md_list),
        align='center',
    )
    static_md_content = File('README.static.md').read()
    md_content = static_md_content.replace("$EXAMPLES", examples_md.content)
    File('README.md').write(md_content)
    log.info('Saved README.md')


def build_examples(force_build):
    image_html_list = []
    for example in Example.list():
        example.run(force_build)
        example.build_markdown()

        image_html_list.append(Markdown.img_html(example.url_animated_gif))


if __name__ == "__main__":
    force_build = len(sys.argv) > 1 and sys.argv[1] == 'force_build'
    build_readme()
    build_examples(force_build)
