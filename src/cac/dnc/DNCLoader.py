import geopandas as gpd
import pandas as pd
import topojson
from utils import JSONFile, Log

log = Log('DNCLoader')


class DNCLoader:
    @classmethod
    def from_topojson(cls, topojson_path, values):
        data = JSONFile(topojson_path).read()
        object_name = list(data['objects'].keys())[0]
        topo = topojson.Topology(data, object_name=object_name)
        gdf = topo.to_gdf()
        return cls(gdf, values)

    @classmethod
    def from_ents(cls, ents, values):
        gdfs = []
        for ent in ents:
            gdf = ent.geo()
            gdfs.append(gdf)
            cls.extract_shapely_polygon(gdf['geometry'][0])

        combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

        return cls(combined_gdf, values)

    @staticmethod
    def get_gdf_from_shapely_polygons(shapely_polygons):
        gdf = gpd.GeoDataFrame()
        gdf['geometry'] = shapely_polygons
        return gdf

    @classmethod
    def from_dnc(cls, dnc, shapely_polygons):
        gdf = DNCLoader.get_gdf_from_shapely_polygons(shapely_polygons)
        return cls(gdf, dnc.values)
