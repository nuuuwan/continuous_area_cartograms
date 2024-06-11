from functools import cache


class Number:
    def __init__(self, x):
        self.x = x

    def humanized(self):
        return self.get_humanized(self.x)

    @staticmethod
    @cache
    def get_humanized(x):
        if isinstance(x, int):
            if x > 1_000_000:
                return f'{x/1_000_000:,.1f}M'
            if x > 1_000:
                return f'{x/1_000:,.1f}K'
            return f'{x:,.0f}'
        if isinstance(x, float):
            return f'{x:,.1g}'

        raise ValueError(f'Value "{str(x)}" is of unknown type: {type(x)}')
