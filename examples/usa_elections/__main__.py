import os

import geopandas as gpd
from utils import JSONFile, Log

from cac import DCN1985, DCN1985AlgoParams, HexBinRenderer

log = Log("usa_elections")


def get_info_idx():
    info_list = JSONFile(
        os.path.join("examples_data", "usa_elections", "prespoll2024.json")
    ).read()
    return {info["State"]: info for info in info_list}


def main():  # noqa

    info_idx = get_info_idx()

    geojson_path = os.path.join(
        "examples_data", "geojson_data", "us-states.geo.json"
    )
    gdf = gpd.read_file(geojson_path)
    values = []

    colors = []
    group_label_to_group = {"all": []}
    for __, row in gdf.iterrows():
        state = row["name"]
        info = info_idx.get(state)

        if info is None:
            log.error(f"info not found for {state}")
            values.append(0)
        else:
            evs = int(round(info["EVs"]))
            values.append(evs)

        mov = info["Forecasted margin of victory"]
        color = "blue" if mov.startswith("D") else "red"
        colors.append(color)

        group_label_to_group["all"].append(state)

    algo = DCN1985.from_geojson(
        geojson_path=geojson_path,
        values=values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=20,
        ),
    )

    _, dcn_list = algo.build(os.path.dirname(__file__))

    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values

    print(labels, values)

    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=538,
    ).write(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
    )


if __name__ == "__main__":
    main()
