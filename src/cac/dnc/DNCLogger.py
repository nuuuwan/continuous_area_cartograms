import math

from utils import Log

log = Log('DNCLogger')


class DNCLogger:
    @staticmethod
    def format_log2_error(x):
        return f'{(2**x):.1%}'

    @staticmethod
    def get_emoji(log2_error, min_log2_error):
        if log2_error > min_log2_error:
            return '🟥'

        if log2_error < -min_log2_error:
            return '🟦'

        return '✅'

    def get_sorted_i_to_log2_error(self):
        return dict(
            sorted(
                [
                    [i, log2_error]
                    for i, log2_error in enumerate(self.Log2Error)
                ],
                key=lambda x: abs(x[1]),
                reverse=True,
            )
        )

    def log_error(self):
        i_to_log2_error = self.get_sorted_i_to_log2_error()
        MAX_DISPLAY = 10
        items = list(i_to_log2_error.items())
        n_all = len(items)
        if n_all > MAX_DISPLAY:
            log.warn(
                f'({MAX_DISPLAY:,}/{n_all:,} '
                + 'highest desired/actual value)'
            )
            items = items[:MAX_DISPLAY]
        for id, log2_error in items:
            emoji = self.get_emoji(log2_error, self.min_log2_error)
            int(math.ceil(abs(log2_error)))
            log.debug(
                f'{id})'.rjust(8)
                + DNCLogger.format_log2_error(log2_error).rjust(8)
                + emoji.rjust(4)
            )
        log.debug(
            'mean(desired/actual value)='
            + DNCLogger.format_log2_error(self.mean_abs_log2_error)
        )
        log.debug(
            '✅ = ' + DNCLogger.format_log2_error(-self.min_log2_error) + ' to ' + DNCLogger.format_log2_error(self.min_log2_error) 
        )

    def log_complexity(self):
        n_polygons = self.n_polygons
        n_points = self.n_points
        complexity = n_polygons * n_points
        log.debug(f'{n_polygons=:,}')
        log.debug(f'{n_points=:,}')
        log.debug(f'{complexity=:,}')
