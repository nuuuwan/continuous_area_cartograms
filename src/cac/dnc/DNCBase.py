from functools import cached_property

from utils import Log

from cac.core import GroupedPolygon, GroupedPolygonGroup, Polygon, PolygonGroup

log = Log('DNCBase')


class DNCBase:
    def __init__(self, id_to_shapely_polygons, id_to_value):
        self.id_to_shapely_polygons = id_to_shapely_polygons
        self.id_to_value = id_to_value

    # shapes
    @cached_property
    def polygons(self):
        polygons = []
        for id, shapely_polygon in self.id_to_shapely_polygons.items():
            polygon = Polygon(
                id, shapely_polygon, self.id_to_value.get(id, 1)
            )
            polygons.append(polygon)

        return polygons

    @cached_property
    def polygon_group(self):
        return PolygonGroup(self.polygons)

    @cached_property
    def grouped_polygons(self):
        polygon_group = self.polygon_group
        return [
            GroupedPolygon(polygon, polygon_group)
            for polygon in self.polygons
        ]

    @cached_property
    def grouped_polygon_group(self):
        return GroupedPolygonGroup(self.grouped_polygons)
