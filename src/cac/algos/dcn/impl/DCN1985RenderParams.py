class DCN1985RenderParams:
    def __init__(
        self,
        super_title: str = None,
        title: str = None,
        sub_title: str = None,
        footer_text: str = None,
        #
        start_value_color: str = None,
        #
        end_value_color: str = None,
    ):
        self.super_title = super_title or ''
        self.title = title or ''
        self.sub_title = sub_title or ''
        self.footer_text = footer_text or ''

        #
        self.start_value_color = start_value_color or 'gray'

        #
        self.end_value_color = end_value_color or self.infer_end_value_color(
            self.title
        )

    def __str__(self) -> str:
        return f'DCN1985RenderParams({str(self.__dict__)})'

    def infer_end_value_color(self, title: str) -> str:
        for phrase, color in [
            ('population', 'red'),
            ('gdp', 'green'),
            ('electors', 'cyan'),
            ('slasscom', 'blue'),
            ('unit', 'lightblue'),
        ]:
            if phrase in title.lower():
                return color
        return 'pink'
