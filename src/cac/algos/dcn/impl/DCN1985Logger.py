from utils import Log

log = Log('DCN1985Logger')


class DCN1985Logger:
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

    def get_sorted_label_to_log2_error(self):
        return dict(
            sorted(
                [
                    [label, log2_error]
                    for label, log2_error in zip(self.labels, self.Log2Error)
                ],
                key=lambda x: abs(x[1]),
                reverse=True,
            )
        )

    def log_error(self):
        label_to_log2_error = self.get_sorted_label_to_log2_error()
        MAX_DISPLAY = 10
        items = list(label_to_log2_error.items())
        n_all = len(items)
        if n_all > MAX_DISPLAY:
            log.warn(
                f'({MAX_DISPLAY:,}/{n_all:,} '
                + 'highest desired/actual value)'
            )
            items = items[:MAX_DISPLAY]
        for label, log2_error in items:
            emoji = self.get_emoji(
                log2_error, self.algo_params.min_log2_error
            )
            log.debug(
                f'{label}'.rjust(24)
                + DCN1985Logger.format_log2_error(log2_error).rjust(12)
                + emoji.rjust(12)
            )
        log.debug(
            'mean(desired/actual value)='
            + DCN1985Logger.format_log2_error(self.mean_abs_log2_error)
        )
        log.debug(
            '✅ = '
            + DCN1985Logger.format_log2_error(-self.algo_params.min_log2_error)
            + ' to '
            + DCN1985Logger.format_log2_error(self.algo_params.min_log2_error)
        )

    def log_complexity(self):
        n_polygons = self.n_polygons
        n_points = self.n_points
        complexity = n_polygons * n_points
        log.debug(f'{n_polygons=:,}')
        log.debug(f'{n_points=:,}')
        log.debug(f'{complexity=:,}')
