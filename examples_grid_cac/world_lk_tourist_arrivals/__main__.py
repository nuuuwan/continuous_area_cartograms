import os

import geopandas

from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, GridCAC
from examples_grid_cac.world_lk_tourist_arrivals.LK_TOURIST_ARRIVALS import (
    LK_TOURIST_ARRIVALS,
)
from examples_grid_cac.world_lk_tourist_arrivals.NAME_MAP_TO_NAME_DATA import (
    NAME_MAP_TO_NAME_DATA,
)

ALGO_PARAMS = DCN1985AlgoParams(
    do_shrink=True,
)


def get_dnc_population():
    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path("naturalearth_lowres")
    )
    gdf_world = gdf_world[gdf_world["continent"] != "Antarctica"]

    values = gdf_world["pop_est"].tolist()
    return DCN1985.from_gdf(
        gdf_world,
        values,
        algo_params=ALGO_PARAMS,
        render_params=DCN1985RenderParams(
            super_title="World",
            title="Population",
            sub_title="2023 Est.",
            footer_text="Data Source: United Nations",
            end_value_color="maroon",
        ),
    )


def get_dnc_gdp():
    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path("naturalearth_lowres")
    )
    gdf_world = gdf_world[gdf_world["continent"] != "Antarctica"]

    values = gdf_world["gdp_md_est"].tolist()
    values = [value * 1_000_000 for value in values]
    return DCN1985.from_gdf(
        gdf_world,
        values,
        algo_params=ALGO_PARAMS,
        render_params=DCN1985RenderParams(
            super_title="World",
            title="Gross Domestic Product (GDP)",
            sub_title="2023 Est. (in USD)",
            footer_text="Data Source: United Nations",
            end_value_color="orange",
        ),
    )


def get_dnc_tourism():  # noqa
    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path("naturalearth_lowres")
    )
    gdf_world = gdf_world[gdf_world["continent"] != "Antarctica"]

    names = []
    values = []
    for name in gdf_world["name"].tolist():
        name_data = NAME_MAP_TO_NAME_DATA.get(name, name)
        value = LK_TOURIST_ARRIVALS.get(name_data)
        if value is None:
            continue
        names.append(name)
        values.append(value)

    gdf_world = gdf_world[gdf_world["name"].isin(names)]

    return DCN1985.from_gdf(
        gdf_world,
        values,
        algo_params=ALGO_PARAMS,
        render_params=DCN1985RenderParams(
            super_title="World",
            title="Tourist Arrivals to Sri Lanka",
            sub_title="2023",
            footer_text="Data Source: United Nations",
            end_value_color="green",
        ),
    )


def main():
    dcn_list_list = [
        [get_dnc_tourism()],
        [get_dnc_gdp()],
        [get_dnc_population()],
    ]
    GridCAC(dcn_list_list).build(os.path.dirname(__file__))


if __name__ == "__main__":
    main()
