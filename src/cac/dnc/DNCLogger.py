from utils import Log

from cac.core import GroupedPolygonGroup

log = Log('DNCLogger')


class DNCLogger:
    @staticmethod
    def log_np(label, x):
        print(label + ".shape", ' ➡️ ', x.shape)
        raise Exception('🛑 Stopped!')

    @staticmethod
    def log_line():
        log.debug('-' * 64)

    @staticmethod
    def get_emoji(log2_error):
        k = GroupedPolygonGroup.MIN_ABS_LOG2_ERROR_FOR_COMPLETION
        if log2_error > k:
            return '🟥'

        if log2_error < -k:
            return '🟦'

        return '✅'

    def get_id_to_log2_error(self):
        return dict(
            sorted(
                [
                    [grouped_polygon.id, grouped_polygon.log2_error]
                    for grouped_polygon in self.grouped_polygons
                ],
                key=lambda x: abs(x[1]),
                reverse=True,
            )
        )

    def log_error(self):
        id_to_log2_error = self.get_id_to_log2_error()
        MAX_DISPLAY = 10
        items = list(id_to_log2_error.items())
        if len(items) > MAX_DISPLAY:
            log.warn(f'({MAX_DISPLAY} highest errors)')
            items = items[:MAX_DISPLAY]
        for id, log2_error in items:
            emoji = self.get_emoji(log2_error)
            log.debug(f' {id} ' + f'{log2_error:.2f} '.rjust(10) + emoji)

    def log_vars(self):
        log.debug(f'total_area = {self.polygon_group.total_area}')
        log.debug(f'total_value = {self.polygon_group.total_value}')

        for grouped_polygon in self.grouped_polygons:
            log.debug(f'id = {grouped_polygon.id}')
            log.debug(f'  value = {grouped_polygon.value}')
            log.debug(f'  centroid = {grouped_polygon.centroid}')
            log.debug(f'  area = {grouped_polygon.area}')

            log.debug(f'  desired = {grouped_polygon.desired}')
            log.debug(f'  mass = {grouped_polygon.mass}')
            log.debug(f'  size_error = {grouped_polygon.size_error}')

        log.debug(
            f'mean_size_error = {self.grouped_polygon_group.mean_size_error}'
        )
        log.debug(
            'force_reduction_factor = '
            + f'{self.grouped_polygon_group.force_reduction_factor}'
        )

    def log_complexity(self):
        n_polygons = self.polygon_group.n_polygons
        n_points = self.polygon_group.n_points
        complexity = n_polygons * n_points
        log.debug(f'{n_polygons=:,}')
        log.debug(f'{n_points=:,}')
        log.debug(f'{complexity=:,}')
