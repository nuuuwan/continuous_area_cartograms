import math

from utils import Log

log = Log('DNCLogger')


class DNCLogger:
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
            log.warn(f'({MAX_DISPLAY:,}/{n_all:,} highest log2_errors)')
            items = items[:MAX_DISPLAY]
        for id, log2_error in items:
            emoji = self.get_emoji(log2_error, self.min_log2_error)
            n_emojis = int(math.ceil(abs(log2_error)))
            emojis = n_emojis * emoji
            log.debug(
                f' {id} '.rjust(6)
                + f'{log2_error:.2f} '.rjust(6)
                + emojis.ljust(6)
            )
        log.debug(f'mean_abs_log2_error={self.mean_abs_log2_error:.4f}')

    def log_complexity(self):
        n_polygons = self.n_polygons
        n_points = self.n_points
        complexity = n_polygons * n_points
        log.debug(f'{n_polygons=:,}')
        log.debug(f'{n_points=:,}')
        log.debug(f'{complexity=:,}')
