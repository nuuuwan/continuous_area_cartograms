import math
import os
from functools import cached_property

from matplotlib import pyplot as plt
from shapely import MultiPolygon as ShapelyMultiPolygon
from shapely import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from utils import JSONFile, Log

import topojson

log = Log('DNC')


class Polygon:
    def __init__(
        self,
        id,
        shapely_polygon,
        value,
    ):
        self.id = id
        self.shapely_polygon = shapely_polygon
        self.value = value

    @cached_property
    def area(self):
        # "Calculate area and centroid (using current boundaries) - 1"
        return self.shapely_polygon.area

    @cached_property
    def centroid(self):
        # "Calculate area and centroid (using current boundaries) - 2"
        return self.shapely_polygon.centroid

    @cached_property
    def radius(self):
        # "Radius = SquareRoot (Area/pi)"
        return math.sqrt(self.area / math.pi)


class PolygonGroup:
    def __init__(self, polygons):
        self.polygons = polygons

    @cached_property
    def total_area(self):
        # "Sum areas into TotalArea"
        return sum(polygon.area for polygon in self.polygons)

    @cached_property
    def total_value(self):
        # "Sum PolygonValue into TotalValue"
        return sum(polygon.value for polygon in self.polygons)


class GroupedPolygon(Polygon, PolygonGroup):
    def __init__(self, polygon, polygon_group):
        Polygon.__init__(
            self, polygon.id, polygon.shapely_polygon, polygon.value
        )
        PolygonGroup.__init__(self, polygon_group.polygons)

    @cached_property
    def desired(self):
        # "Desired = (TotalArea * (PolygonValue / TotalValue))"
        return self.total_area * self.value / self.total_value

    @cached_property
    def mass(self):
        # Mass = SquareRoot (Desired / pi) - SquareRoot (Area / pi)
        return math.sqrt(self.desired / math.pi) - self.radius

    @cached_property
    def size_error(self):
        # "SizeError = Max(Area, Desired) / Min(Area, Desired)"
        return max(self.area, self.desired) / min(self.area, self.desired)


class GroupPolygonGroup:
    def __init__(self, grouped_polygons):
        self.grouped_polygons = grouped_polygons

    @cached_property
    def mean_size_error(self):
        s = sum(
            grouped_polygon.size_error
            for grouped_polygon in self.grouped_polygons
        )
        n = len(self.grouped_polygons)
        return s / n

    @cached_property
    def force_reduction_factor(self):
        # "ForceReductionFactor = 1 / (1 + Mean (SizeError))"
        return 1 / (1 + self.mean_size_error)


class DNC:
    def __init__(self, topo_path, id_to_value):
        self.topo_path = topo_path
        self.id_to_value = id_to_value

    # Helpers
    @cached_property
    def topo(self):
        data = JSONFile(self.topo_path).read()
        objects = data['objects']
        objects_name = list(objects.keys())[0]
        geometries = objects[objects_name]['geometries']
        n_geometries = len(geometries)
        log.debug(f'Read {n_geometries} {objects_name} from {self.topo_path}')
        topo = topojson.Topology(data, object_name=objects_name)
        return topo

    @cached_property
    def polygons(self):
        geometries = self.gdf['geometry']
        id_nums = self.gdf['dis_c']

        shapely_polygons = []
        ids = []
        for geometry, id_num in zip(geometries, id_nums):
            if isinstance(geometry, ShapelyPolygon):
                shapely_polygon = geometry
            elif isinstance(geometry, ShapelyMultiPolygon):
                shapely_polygon = max(
                    geometry.geoms,
                    key=lambda polygon: polygon.area,
                )
            else:
                raise ValueError(f'Unknown geometry type {type(geometry)}')
            id = 'LK-' + str(id_num)
            shapely_polygons.append(shapely_polygon)
            ids.append(id)

        polygons = []
        for id, shapely_polygon in zip(ids, shapely_polygons):
            polygon = Polygon(
                id, shapely_polygon, self.id_to_value.get(id, 1)
            )
            polygons.append(polygon)

        polygons.sort(key=lambda polygon: polygon.id)
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
    def group_polygon_group(self):
        return GroupPolygonGroup(self.grouped_polygons)

    # Algorithms
    def run(self):
        # "For each boundary line; Read coordinate chain"
        #     "For each coordinate pair"
        new_shapely_polygons = []
        for polygon in self.grouped_polygons:
            log.debug(f'Processing {polygon.id}...')
            new_points = []
            for point in polygon.shapely_polygon.exterior.coords:
                dx, dy = 0, 0
                # "For each polygon centroid"
                for polygon0 in self.grouped_polygons:
                    centroid = polygon0.centroid

                    # "Find angle, Distance from centroid to coordinate"
                    distance = centroid.distance(ShapelyPoint(point))
                    angle = math.atan2(
                        point[1] - centroid.y, point[0] - centroid.x
                    )
                    # "If (Distance > Radius of polygon)"
                    if distance > polygon0.radius:
                        # "Fij = Mas * (Radius / Distance)"
                        fij = polygon0.mass * (polygon0.radius / distance)
                    # "Else"
                    else:
                        # "Fij = Mass * (Distance ^ 2 / Radius ^ 2)
                        #     * (4 - 3 * (Distance / Radius))"
                        fij = (
                            polygon0.mass
                            * (distance**2 / polygon0.radius**2)
                            * (4 - 3 * (distance / polygon0.radius))
                        )

                    # "Using Fij and angles, calculate vector sum"
                    # "Multiply by ForceReductionFactor"
                    frf = self.group_polygon_group.force_reduction_factor
                    k = frf * fij
                    dx += k * math.cos(angle)
                    dy += k * math.sin(angle)
                # Move coordinate accordingly
                new_point = (point[0] + dx, point[1] + dy)
                new_points.append(new_point)
            new_shapely_polygon = ShapelyPolygon(new_points)
            new_shapely_polygons.append(new_shapely_polygon)

        topo = topojson.Topology(new_shapely_polygons)
        JSONFile(os.path.join('topojson', 'converted.json')).write(
            topo.to_json()
        )
        gdf = topo.to_gdf()
        DNC.save_image(gdf, os.path.join('images', 'converted.png'))

    # Render
    @cached_property
    def gdf(self):
        return self.topo.to_gdf()

    @staticmethod
    def save_image(gdf, image_path):
        plt.close()
        gdf.plot()
        plt.savefig(image_path, dpi=300)
        log.info(f'Wrote {image_path}')


if __name__ == "__main__":
    topo_path = os.path.join('topojson', 'Districts.json')
    dnc = DNC(topo_path, {'LK-11': 100})
    DNC.save_image(dnc.gdf, os.path.join('images', 'original.png'))

    log.debug('Polygon[0]')
    polygon = dnc.polygons[0]
    log.debug(f'  id = {polygon.id}')
    log.debug(f'  value = {polygon.value}')
    log.debug(f'  centroid = {polygon.centroid}')
    log.debug(f'  area = {polygon.area}')

    log.debug('PolygonGroup')
    log.debug(f'  total_area = {dnc.polygon_group.total_area}')
    log.debug(f'  total_value = {dnc.polygon_group.total_value}')

    log.debug('GroupedPolygon[0]')
    grouped_polygon = dnc.grouped_polygons[0]
    log.debug(f'  desired = {grouped_polygon.desired}')
    log.debug(f'  mass = {grouped_polygon.mass}')
    log.debug(f'  size_error = {grouped_polygon.size_error}')

    log.debug('GroupPolygonGroup')
    log.debug(
        f'  mean_size_error = {dnc.group_polygon_group.mean_size_error}'
    )
    log.debug(
        '  force_reduction_factor = '
        + f'{dnc.group_polygon_group.force_reduction_factor}'
    )

    dnc.run()
