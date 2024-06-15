from utils import File, Log

log = Log('Markdown')


class Markdown:
    BLANK_LINE = ''
    TAB = ' ' * 4

    def __init__(self, *lines):
        for line in lines:
            if not isinstance(line, str):
                raise ValueError(
                    f'Expected str, got {type(line)}: {str(line)}'
                )
        self.lines = list(lines)

    @property
    def lines_tabbed(self):
        return [Markdown.TAB + line for line in self.lines]

    @property
    def content(self):
        return '\n'.join(self.lines)

    @property
    def content_tabbed(self):
        return '\n'.join(self.lines_tabbed)

    @property
    def lines_cleaned(self):
        lines = [line.rstrip() for line in self.lines]
        content = '\n'.join(lines)
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        return content.split('\n')

    def __add__(self, other):
        if isinstance(other, Markdown):
            self.lines += other.lines
            return self

        raise ValueError(f'Cannot add {type(other)} to Markdown')

    def save(self, file_path):
        File(file_path).write_lines(self.lines_cleaned)
        log.info(f'Saved {file_path}')

    # simple objects

    @staticmethod
    def bold(md):
        return Markdown(f'*{md.content}*')

    @staticmethod
    def italic(md):
        return Markdown(f'*{md.content}*')

    @staticmethod
    def link(url, md=None):
        if md is None:
            md = Markdown([url])
        return Markdown(f'[{md.content}]({url})')

    @staticmethod
    def image(url, alt_text=None):
        if alt_text is None:
            alt_text = url
        return Markdown(f'![{alt_text}]({url})')





    @staticmethod
    def hx(level, title_md, *body_md_list):
        return Markdown(
            ('#' * level) + ' ' + title_md.content,
            *[body_md.content for body_md in body_md_list],
            Markdown.BLANK_LINE,
        )

    @staticmethod
    def h1(title_md, *body_md_list):
        return Markdown.hx(1, title_md, *body_md_list)

    @staticmethod
    def h2(title_md, *body_md_list):
        return Markdown.hx(2, title_md, *body_md_list)

    @staticmethod
    def h3(title_md, *body_md_list):
        return Markdown.hx(3, title_md, *body_md_list)

    # complex objects
    @staticmethod
    def code(lang, child_md):
        return Markdown(
            Markdown.BLANK_LINE,
            f'```{lang}',
            child_md.content,
            '```',
            Markdown.BLANK_LINE,
        )
    
    # html 

    @staticmethod
    def p_html(child_md, align=None):
        align_str = ''
        if align is not None:
            align_str = f' align="{align}"'
        return Markdown(
            Markdown.BLANK_LINE,
            f'<p {align_str}>',
            child_md.content_tabbed,
            '</p>',
            Markdown.BLANK_LINE,
        )


    @staticmethod
    def img_html(url, alt_text=None, width=None):
        if alt_text is None:
            alt_text = url
        width_str = ''
        if width is not None:
            width_str = f' width="{width}"'
        return Markdown(
            f'<img src="{url}" alt="{alt_text}" {width_str} />',
        )