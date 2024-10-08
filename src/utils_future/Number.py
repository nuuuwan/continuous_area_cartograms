from functools import cache


class Number:
    def __init__(self, x):
        self.x = x

    def humanized(self):
        return self.get_humanized(self.x)

    @staticmethod
    @cache
    def get_humanized(x):
        if x > 1_000_000_000:
            return f'{x/1_000_000_000.0:,.1f}B'
        if x > 1_000_000:
            return f'{x/1_000_000.0:,.1f}M'
        if x > 1_000:
            return f'{x/1_000.0:,.1f}K'
        if x > 1:
            return f'{x:,.0f}'
        return f'{x:.1g}'
