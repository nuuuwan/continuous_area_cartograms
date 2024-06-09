import math
import os
from functools import cached_property

from gig import Ent, EntType
from matplotlib import pyplot as plt
from shapely import MultiPolygon as ShapelyMultiPolygon
from shapely import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from utils import JSONFile, Log

import topojson
from cac.core import GroupedPolygon, GroupPolygonGroup, Polygon, PolygonGroup

log = Log('DNC')


class DNC:
    def __init__(self, id_to_shapely_polygons, id_to_value):
        self.id_to_shapely_polygons = id_to_shapely_polygons
        self.id_to_value = id_to_value

    # loaders
    @staticmethod
    def extract_shapely_polygon(geometry):
        if isinstance(geometry, ShapelyPolygon):
            return geometry

        if isinstance(geometry, ShapelyMultiPolygon):
            return max(
                geometry.geoms,
                key=lambda polygon: polygon.area,
            )

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @staticmethod
    def from_topojson(topojson_path, get_ids, id_to_value):
        data = JSONFile(topojson_path).read()
        objects = data['objects']
        objects_name = list(objects.keys())[0]
        geometries = objects[objects_name]['geometries']
        n_geometries = len(geometries)
        log.debug(f'Read {n_geometries} {objects_name} from {topojson_path}')
        topo = topojson.Topology(data, object_name=objects_name)
        gdf = topo.to_gdf()
        geometries = gdf['geometry']
        id_nums = get_ids(gdf)

        id_to_shapely_polygons = {}
        for geometry, id_num in zip(geometries, id_nums):
            id = 'LK-' + str(id_num)
            shapely_polygon = DNC.extract_shapely_polygon(geometry)
            id_to_shapely_polygons[id] = shapely_polygon

        return DNC(id_to_shapely_polygons, id_to_value)

    @staticmethod
    def from_ents(ents, id_to_value):
        id_to_shapely_polygons = {}
        for ent in ents:
            gdf = ent.geo()

            shapely_polygon = DNC.extract_shapely_polygon(gdf['geometry'][0])
            id_to_shapely_polygons[ent.id] = shapely_polygon
        return DNC(id_to_shapely_polygons, id_to_value)

    # shapes
    @cached_property
    def polygons(self):
        polygons = []
        for id, shapely_polygon in self.id_to_shapely_polygons.items():
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

    # algorithm
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

        return new_shapely_polygons

    # render
    @staticmethod
    def save_image(shapely_polygons, image_path):
        gdf = topojson.Topology(shapely_polygons).to_gdf()
        plt.close()
        gdf.plot()
        plt.savefig(image_path, dpi=300)
        log.info(f'Wrote {image_path}')

    # testing
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


def test_from_topojson():
    # dnc = DNC.from_topojson(
    #     os.path.join('topojson', 'Provinces.json'),
    #     lambda gdf: gdf['prov_c'],
    #     {},
    # )

    dnc = DNC.from_topojson(
        os.path.join('topojson', 'Districts.json'),
        lambda gdf: gdf['dis_c'],
        {},
    )

    # dnc = DNC.from_topojson(
    #     os.path.join('topojson', 'DSDivisions.json'),
    #     lambda gdf: gdf['dsd_c'],
    #     {},
    # )

    DNC.save_image(
        list(dnc.id_to_shapely_polygons.values()),
        os.path.join('images', 'original.topojson.png'),
    )
    shapely_polygons = dnc.run()
    DNC.save_image(
        shapely_polygons, os.path.join('images', 'converted.topojson.png')
    )


def test_from_ents():
    ents = [
        ent
        for ent in Ent.list_from_type(EntType.DISTRICT)
        if ent.id in ['LK-11', 'LK-12', 'LK-13', 'LK-91', 'LK-92']
    ]
    id_to_value = {}
    total_population = sum(ent.population for ent in ents)
    for ent in ents:
        population = ent.population
        value = (population / total_population) ** 2
        log.debug(f'{ent.id} = {value}')
        id_to_value[ent.id] = value

    dnc = DNC.from_ents(ents, id_to_value)

    DNC.save_image(
        list(dnc.id_to_shapely_polygons.values()),
        os.path.join('images', 'original.ents.png'),
    )
    shapely_polygons = dnc.run()
    DNC.save_image(
        shapely_polygons, os.path.join('images', 'converted.ents.png')
    )


if __name__ == "__main__":
    # test_from_topojson()
    test_from_ents()
