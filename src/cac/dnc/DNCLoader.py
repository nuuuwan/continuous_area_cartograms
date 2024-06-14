import geopandas as gpd
import pandas as pd
import topojson
from gig import Ent
from shapely.geometry import MultiPolygon, Polygon
from utils import JSONFile, Log

log = Log('DNCLoader')


class DNCLoader:
    @staticmethod
    def extract_polygons(geometry) -> list[Polygon]:
        if isinstance(geometry, Polygon):
            return [geometry]

        if isinstance(geometry, MultiPolygon):
            return geometry.geoms

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @classmethod
    def from_gdf(cls, gdf: gpd.GeoDataFrame, values: list[float], **kwargs):
        geometry = gdf['geometry']
        min_p_area = kwargs.get('min_p_area', 0.01)

        polygons_for_dnc = []
        values_for_dnc = []
        for value, shape in zip(values, geometry):
            polygons = DNCLoader.extract_polygons(shape)

            total_area = sum([polygon.area for polygon in polygons])
            min_area = total_area * min_p_area
            filtered_polygons = [
                polygon for polygon in polygons if polygon.area > min_area
            ]
            total_area = sum([polygon.area for polygon in filtered_polygons])
            values_for_shape = [
                value * polygon.area / total_area
                for polygon in filtered_polygons
            ]
            polygons_for_dnc.extend(filtered_polygons)
            values_for_dnc.extend(values_for_shape)
        return cls(polygons_for_dnc, values_for_dnc, **kwargs)

    @classmethod
    def from_geojson(cls, geojson_path: str, values: list[float], **kwargs):
        gdf = gpd.read_file(geojson_path)
        return cls.from_gdf(gdf, values, **kwargs)

    @classmethod
    def from_topojson(cls, topojson_path: str, values: list[float], **kwargs):
        data = JSONFile(topojson_path).read()
        object_name = list(data['objects'].keys())[0]
        topo = topojson.Topology(data, object_name=object_name)
        gdf = topo.to_gdf()
        return cls.from_gdf(gdf, values, **kwargs)

    @classmethod
    def from_ents(cls, ents: list[Ent], values: list[float], **kwargs):
        gdfs = []
        for ent in ents:
            gdf = ent.geo()
            gdfs.append(gdf)

        combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
        return cls.from_gdf(combined_gdf, values, **kwargs)

    def to_gdf(self):
        return gpd.GeoDataFrame(
            {
                'geometry': self.polygons,
                'value': self.values,
            }
        )

    def from_dnc(self, polygons, **kwargs):
        return self.__class__(
            polygons,
            self.values,
            self.preprocess_tolerance,
            self.min_log2_error,
            self.max_iterations,
            **kwargs,
        )
