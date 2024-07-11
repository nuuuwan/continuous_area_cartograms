import geopandas as gpd
import pandas as pd
import topojson
from gig import Ent
from utils import JSONFile, Log

from cac.algos.dcn.impl.DCN1985AlgoParams import DCN1985AlgoParams
from cac.algos.dcn.impl.DCN1985LoaderUtils import DCN1985LoaderUtils

log = Log('DCN1985Loader')


class DCN1985Loader(DCN1985LoaderUtils):
    @classmethod
    def from_gdf(
        cls,
        gdf: gpd.GeoDataFrame,
        values: list[float] = ModuleNotFoundError,
        algo_params=None,
        render_params=None,
    ):
        algo_params = algo_params or DCN1985AlgoParams()
        geometry = gdf['geometry']
        labels = cls.get_labels(gdf)

        values = values or [1 for _ in range(len(geometry))]

        min_p_area = algo_params.min_p_area

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

        return cls(
            polygons_for_dcn,
            values_for_dcn,
            labels_for_dcn,
            algo_params,
            render_params,
        )

    @classmethod
    def from_geojson(
        cls,
        geojson_path: str,
        values: list[float] = None,
        algo_params=None,
        render_params=None,
    ):
        gdf = gpd.read_file(geojson_path)
        return cls.from_gdf(gdf, values, algo_params, render_params)

    @classmethod
    def from_topojson(
        cls,
        topojson_path: str,
        values: list[float] = None,
        algo_params=None,
        render_params=None,
    ):
        data = JSONFile(topojson_path).read()
        object_name = list(data['objects'].keys())[0]
        topo = topojson.Topology(data, object_name=object_name)
        gdf = topo.to_gdf()
        gdf.to_file('Provinces.geo.json', driver='GeoJSON')
        return cls.from_gdf(gdf, values, algo_params, render_params)

    @classmethod
    def from_ents(
        cls,
        ents: list[Ent],
        values: list[float] = None,
        algo_params=None,
        render_params=None,
    ):
        gdfs = []
        for ent in ents:
            gdf = ent.geo()
            log.debug(f'Loaded geo for {ent.id}')
            gdfs.append(gdf)

        combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
        combined_gdf['id'] = [ent.id for ent in ents]
        combined_gdf['name'] = [ent.name for ent in ents]
        return cls.from_gdf(combined_gdf, values, algo_params, render_params)

    def to_gdf(self):
        return gpd.GeoDataFrame(
            {
                'geometry': self.polygons,
                'value': self.values,
            }
        )

    def from_dcn(self, polygons=None):
        return self.__class__(
            polygons or self.polygons,
            self.values,
            self.labels,
            self.algo_params,
            self.render_params,
        )
