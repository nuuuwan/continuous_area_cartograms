import math
import os
from functools import cache, cached_property

from gig import Ent, EntType
from matplotlib import pyplot as plt
from shapely import MultiPolygon as ShapelyMultiPolygon
from shapely import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from utils import JSONFile, Log

import topojson
from cac.core import GroupedPolygon, GroupPolygonGroup, Polygon, PolygonGroup
from utils_future import AnimatedGIF

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
    def run_single(self):
        # "For each boundary line; Read coordinate chain"
        #     "For each coordinate pair"
        new_shapely_polygons = []
        log.debug(
            f'mean_size_error = {self.group_polygon_group.mean_size_error:.4f}'
        )
        for grouped_polygon in self.grouped_polygons:
            log2_error = grouped_polygon.log2_error
            if log2_error > 0.5:
                emoji = '🔴'
            elif log2_error > -0.5:
                emoji = '🟢'
            else:
                emoji = '🔵'
            log.debug(
                f'  {grouped_polygon.id} '
                + f'{log2_error:.2f} '.rjust(10) + emoji
            )
        for polygon in self.grouped_polygons:
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
                        q = distance / polygon0.radius
                        fij = polygon0.mass * (q**2) * (4 - 3 * q)

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

    def run(self, file_label, n=1):
        assert file_label
        assert n > 0

        dir_path = os.path.join(
            'images',
            file_label,
        )
        os.makedirs(dir_path, exist_ok=True)

        dnc = self
        shapely_polygons = list(dnc.id_to_shapely_polygons.values())
        image_path_list = []
        for i in range(n):
            log.debug(f'run: {i=}')

            image_path = os.path.join(dir_path, f'{i}.png')
            DNC.save_image(
                dnc.grouped_polygons,
                image_path,
            )
            image_path_list.append(image_path)

            shapely_polygons = dnc.run_single()
            ids = list(dnc.id_to_shapely_polygons.keys())
            id_to_shapely_polygons = {
                id: shapely_polygon
                for id, shapely_polygon in zip(ids, shapely_polygons)
            }
            dnc = DNC(id_to_shapely_polygons, dnc.id_to_value)

        image_path = os.path.join(dir_path, f'{n}.png')
        DNC.save_image(
            dnc.grouped_polygons,
            image_path,
        )
        image_path_list.append(image_path)

        animated_gif_path = os.path.join(dir_path, 'animated.gif')
        AnimatedGIF(animated_gif_path).write(image_path_list)

        return shapely_polygons

    # render
    @staticmethod
    @cache
    def get_color(log2_error):
        log2_error = max(min(log2_error, 1), -1)
        p = (log2_error + 1) / 2
        r, g, b = [int(c * 255) for c in plt.cm.jet(p)[:3]]
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def save_image(grouped_polygons, image_path):
        plt.close()
        ax = plt.gca()
        for i, grouped_polygon in enumerate(grouped_polygons):
            shapely_polygon = grouped_polygon.shapely_polygon
            log2_error = grouped_polygon.log2_error
            gdf = topojson.Topology(shapely_polygon).to_gdf()
            gdf.plot(
                ax=ax,
                facecolor=DNC.get_color(log2_error),
                edgecolor="white",
                linewidth=0.1,
            )

        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0)
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



