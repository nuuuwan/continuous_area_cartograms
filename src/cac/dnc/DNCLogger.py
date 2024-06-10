from utils import Log

from cac.core import GroupPolygonGroup

log = Log('DNCLogger')


class DNCLogger:
    @staticmethod
    def get_emoji(log2_error):
        k = GroupPolygonGroup.MIN_ABS_LOG2_ERROR_FOR_COMPLETION
        if log2_error > k:
            return '🔴'

        if log2_error < -k:
            return '🔵'

        return '✅'

    def get_id_to_log2_error(self):
        items = {
            grouped_polygon.id: grouped_polygon.log2_error
            for grouped_polygon in self.grouped_polygons
        }.items()

        return dict(
            sorted(
                items,
                key=lambda x: abs(x[1]),
            )
        )

    def log_error(self):
        id_to_log2_error = self.get_id_to_log2_error()
        MAX_DISPLAY = 10
        for id, log2_error in list(id_to_log2_error.items())[:MAX_DISPLAY]:
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
            f'mean_size_error = {self.group_polygon_group.mean_size_error}'
        )
        log.debug(
            'force_reduction_factor = '
            + f'{self.group_polygon_group.force_reduction_factor}'
        )
