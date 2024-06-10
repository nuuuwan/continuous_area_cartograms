from utils import Log

log = Log('DNCLogger')


class DNCLogger:
    def log_vars(dnc):
        log.debug(f'total_area = {dnc.polygon_group.total_area}')
        log.debug(f'total_value = {dnc.polygon_group.total_value}')

        print()
        for grouped_polygon in dnc.grouped_polygons:
            log.debug(f'id = {grouped_polygon.id}')
            log.debug(f'  value = {grouped_polygon.value}')
            log.debug(f'  centroid = {grouped_polygon.centroid}')
            log.debug(f'  area = {grouped_polygon.area}')

            log.debug(f'  desired = {grouped_polygon.desired}')
            log.debug(f'  mass = {grouped_polygon.mass}')
            log.debug(f'  size_error = {grouped_polygon.size_error}')

        print()
        log.debug(
            f'mean_size_error = {dnc.group_polygon_group.mean_size_error}'
        )
        log.debug(
            'force_reduction_factor = '
            + f'{dnc.group_polygon_group.force_reduction_factor}'
        )
