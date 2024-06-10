from utils import Log

log = Log('DNCLogger')


class DNCLogger:
    def log_error(self):
        log.debug(
            f'mean_size_error = {self.group_polygon_group.mean_size_error:.4f}'
        )
        for grouped_polygon in self.grouped_polygons:
            log2_error = grouped_polygon.log2_error
            if log2_error > 0.1:
                emoji = '🔴'
            elif log2_error > -0.1:
                emoji = '🟢'
            else:
                emoji = '🔵'
            log.debug(
                f' {grouped_polygon.id} '
                + f'{log2_error:.2f} '.rjust(10)
                + emoji
            )

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
