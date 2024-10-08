import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from utils import Log

log = Log('DCN1985LoaderUtils')


class DCN1985LoaderUtils:
    @staticmethod
    def extract_polygons(geometry) -> list[Polygon]:
        if isinstance(geometry, Polygon):
            return [geometry]

        if isinstance(geometry, MultiPolygon):
            return sorted(
                geometry.geoms,
                key=lambda polygon: polygon.area,
                reverse=True,
            )

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @staticmethod
    def get_polygons(shape, min_p_area):
        polygons = DCN1985LoaderUtils.extract_polygons(shape)
        total_area = sum([polygon.area for polygon in polygons])
        min_area = total_area * min_p_area
        polygons = [
            polygon for polygon in polygons if polygon.area > min_area
        ]
        sorted_polygons = sorted(
            polygons,
            key=lambda polygon: polygon.area,
            reverse=True,
        )
        return [sorted_polygons[0]]

    @staticmethod
    def get_shape_vars(shape, value, label, min_p_area):
        filtered_polygons = DCN1985LoaderUtils.get_polygons(shape, min_p_area)
        total_area = sum([polygon.area for polygon in filtered_polygons])
        values_for_shape = [
            value * polygon.area / total_area for polygon in filtered_polygons
        ]
        labels_for_shape = [
            (f'{label}-{i+1}' if (i > 0) else label)
            for i in range(len(filtered_polygons))
        ]

        return [filtered_polygons, values_for_shape, labels_for_shape]

    @staticmethod
    def get_labels(gdf: gpd.GeoDataFrame):
        geometry = gdf['geometry']
        labels = None
        if 'name' in gdf:
            labels = gdf['name']
        elif 'id' in gdf:
            labels = gdf['id']
        if labels is None:
            labels = [str(i) for i in range(len(geometry))]
        return labels
