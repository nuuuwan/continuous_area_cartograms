import math

from utils import Log

from cac.core import GroupedPolygonGroup

log = Log('DNCLogger')


class DNCLogger:
    @staticmethod
    def get_emoji(log2_error):
        k = GroupedPolygonGroup.MIN_ABS_LOG2_ERROR_FOR_COMPLETION
        if log2_error > k:
            return '🟥'

        if log2_error < -k:
            return '🟦'

        return '✅'

    def get_sorted_i_to_log2_error(self):
        return dict(
            sorted(
                [
                    [i, grouped_polygon.log2_error]
                    for i, grouped_polygon in enumerate(self.grouped_polygons)
                ],
                key=lambda x: abs(x[1]),
                reverse=True,
            )
        )

    def log_error(self):
        i_to_log2_error = self.get_sorted_i_to_log2_error()
        MAX_DISPLAY = 10
        items = list(i_to_log2_error.items())
        if len(items) > MAX_DISPLAY:
            log.warn(f'({MAX_DISPLAY} highest errors)')
            items = items[:MAX_DISPLAY]
        for id, log2_error in items:
            emoji = self.get_emoji(log2_error)
            n_emojis = int(math.ceil(abs(log2_error)))
            emojis = n_emojis * emoji
            log.debug(
                f' {id} '.rjust(10)
                + f'{log2_error:.2f} '.rjust(10)
                + emojis.rjust(10)
            )

    def log_complexity(self):
        n_polygons = self.polygon_group.n_polygons
        n_points = self.polygon_group.n_points
        complexity = n_polygons * n_points
        log.debug(f'{n_polygons=:,}')
        log.debug(f'{n_points=:,}')
        log.debug(f'{complexity=:,}')
