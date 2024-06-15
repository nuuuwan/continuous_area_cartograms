from utils import File, Log

log = Log('Markdown')


class Markdown:
    BLANK_LINE = ''
    TAB = ' ' * 4

    def __init__(self, lines=None):
        self.lines = lines or []

    def add_blank_line(self):
        self.lines.append(Markdown.BLANK_LINE)

    @property
    def lines_tabbed(self):
        return [Markdown.TAB + line for line in self.lines]

    @property
    def line(self):
        return self.lines[0]

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
    def bold(text):
        return Markdown([f'**{text}**'])

    @staticmethod
    def italic(text):
        return Markdown([f'*{text}*'])

    @staticmethod
    def link(url, text=None):
        if text is None:
            text = url
        return Markdown([f'[{text}]({url})'])

    @staticmethod
    def image(url, alt_text=None):
        if alt_text is None:
            alt_text = url
        return Markdown([f'![{alt_text}]({url})'])

    @staticmethod
    def hx(text, level):
        return Markdown([('#' * level) + ' ' + text, Markdown.BLANK_LINE])

    @staticmethod
    def h1(text):
        return Markdown.hx(text, 1)

    @staticmethod
    def h2(text):
        return Markdown.hx(text, 2)

    @staticmethod
    def h3(text):
        return Markdown.hx(text, 3)

    # complex objects
    @staticmethod
    def code(lang, child):
        return Markdown(
            [
                f'```{lang}',
            ]
            + child.lines
            + [
                '```',
                Markdown.BLANK_LINE,
            ]
        )

    @staticmethod
    def align(alignment, child):
        return Markdown(
            [
                f'<p align="{alignment}">',
            ]
            + child.lines_tabbed
            + ['</p>', Markdown.BLANK_LINE]
        )
