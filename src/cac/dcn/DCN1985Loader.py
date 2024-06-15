import geopandas as gpd
import pandas as pd
import topojson
from gig import Ent
from shapely.geometry import MultiPolygon, Polygon
from utils import JSONFile, Log

log = Log('DCN1985Loader')


class DCN1985Loader:
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
    def get_shape_vars(shape, value, label, min_p_area):
        polygons = DCN1985Loader.extract_polygons(shape)
        total_area = sum([polygon.area for polygon in polygons])
        min_area = total_area * min_p_area
        filtered_polygons = [
            polygon for polygon in polygons if polygon.area > min_area
        ]
        total_area = sum([polygon.area for polygon in filtered_polygons])
        values_for_shape = [
            value * polygon.area / total_area for polygon in filtered_polygons
        ]
        labels_for_shape = [
            (f'{label}-{i+1}' if (i > 0) else label)
            for i in range(len(filtered_polygons))
        ]

        return [filtered_polygons, values_for_shape, labels_for_shape]

    @classmethod
    def from_gdf(
        cls, gdf: gpd.GeoDataFrame, values: list[float] = None, **kwargs
    ):
        geometry = gdf['geometry']

        # labels
        labels = None
        if 'name' in gdf:
            labels = gdf['name']
        elif 'id' in gdf:
            labels = gdf['id']
        if labels is None:
            labels = [str(i) for i in range(len(geometry))]

        # values
        if values is None:
            values = [1 for _ in range(len(geometry))]

        min_p_area = kwargs.get('min_p_area', 0.01)

        polygons_for_dcn = []
        values_for_dcn = []
        labels_for_dcn = []
        for shape, value, label in zip(geometry, values, labels):
            (
                filtered_polygons,
                values_for_shape,
                labels_for_shape,
            ) = DCN1985Loader.get_shape_vars(shape, value, label, min_p_area)
            polygons_for_dcn.extend(filtered_polygons)
            values_for_dcn.extend(values_for_shape)
            labels_for_dcn.extend(labels_for_shape)

        return cls(polygons_for_dcn, values_for_dcn, labels_for_dcn, **kwargs)

    @classmethod
    def from_geojson(
        cls, geojson_path: str, values: list[float] = None, **kwargs
    ):
        gdf = gpd.read_file(geojson_path)
        return cls.from_gdf(gdf, values, **kwargs)

    @classmethod
    def from_topojson(
        cls, topojson_path: str, values: list[float] = None, **kwargs
    ):
        data = JSONFile(topojson_path).read()
        object_name = list(data['objects'].keys())[0]
        topo = topojson.Topology(data, object_name=object_name)
        gdf = topo.to_gdf()
        gdf.to_file('Provinces.geo.json', driver='GeoJSON')
        return cls.from_gdf(gdf, values, **kwargs)

    @classmethod
    def from_ents(cls, ents: list[Ent], values: list[float] = None, **kwargs):
        gdfs = []
        for ent in ents:
            gdf = ent.geo()
            gdfs.append(gdf)

        combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
        combined_gdf['id'] = [ent.id for ent in ents]
        combined_gdf['name'] = [ent.name for ent in ents]
        return cls.from_gdf(combined_gdf, values, **kwargs)

    def to_gdf(self):
        return gpd.GeoDataFrame(
            {
                'geometry': self.polygons,
                'value': self.values,
            }
        )

    def from_dcn(self, polygons, **kwargs):
        return self.__class__(
            polygons,
            self.values,
            self.labels,
            self.preprocess_tolerance,
            self.min_log2_error,
            self.max_iterations,
            self.do_shrink,
            **kwargs,
        )
