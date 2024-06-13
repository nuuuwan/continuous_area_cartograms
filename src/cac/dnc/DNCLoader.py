import geopandas as gpd
import pandas as pd
import topojson
from gig import Ent
from shapely.geometry import MultiPolygon, Polygon
from utils import JSONFile, Log

log = Log('DNCLoader')


class DNCLoader:
    @staticmethod
    def extract_polygon_base(geometry):
        if isinstance(geometry, Polygon):
            return geometry

        if isinstance(geometry, MultiPolygon):
            # TODO: Support MultiPolygon
            return max(
                geometry.geoms,
                key=lambda polygon: polygon.area,
            )

        raise ValueError(f'Unknown geometry type {type(geometry)}')

    @classmethod
    def from_gdf(cls, gdf: gpd.GeoDataFrame, values: list[float]):
        geometry = gdf['geometry']
        polygons = [cls.extract_polygon_base(g) for g in geometry]
        return cls(polygons, values)

    @classmethod
    def from_geojson(cls, geojson_path: str, values: list[float]):
        gdf = gpd.read_file(geojson_path)
        return cls.from_gdf(gdf, values)

    @classmethod
    def from_topojson(cls, topojson_path: str, values: list[float]):
        data = JSONFile(topojson_path).read()
        object_name = list(data['objects'].keys())[0]
        topo = topojson.Topology(data, object_name=object_name)
        gdf = topo.to_gdf()
        return cls.from_gdf(gdf, values)

    @classmethod
    def from_ents(cls, ents: list[Ent], values: list[float]):
        gdfs = []
        for ent in ents:
            gdf = ent.geo()
            gdfs.append(gdf)

        combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
        return cls.from_gdf(combined_gdf, values)

    def to_gdf(self):
        return gpd.GeoDataFrame(
            {
                'geometry': self.polygons,
                'value': self.values,
            }
        )
