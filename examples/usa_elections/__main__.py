import os

import geopandas as gpd
from shapely import Point
from utils import JSONFile, Log, _

from cac import DCN1985, DCN1985AlgoParams, HexBinRenderer
from utils_future import Color

log = Log("usa_elections")


def get_info_idx():
    info_list = JSONFile(
        os.path.join("examples_data", "usa_elections", "prespoll2024.json")
    ).read()
    return {info["State"]: info for info in info_list}


def get_state_to_code():
    return JSONFile(
        os.path.join("examples_data", "usa_elections", "state_to_code.json")
    ).read()


def get_color(info):
    mov = info["Forecasted margin of victory"]
    margin = float(mov[2:])

    MARGIN_UNCERTAIN = 1
    MARGIN_CERTAIN = 10
    LIGHT_MIN, LIGHT_MAX = 50, 80
    if margin < MARGIN_UNCERTAIN:
        hue = 45
        p_light = 0.5
    else:
        party = mov[0]
        hue = 240 if party == "D" else 0
        margin = float(mov[2:])
        if margin > MARGIN_CERTAIN:
            p_light = 0
        else:
            p_light = 1 - (margin - MARGIN_UNCERTAIN) / (
                MARGIN_CERTAIN - MARGIN_UNCERTAIN
            )

    sat = 100
    light = LIGHT_MIN + (LIGHT_MAX - LIGHT_MIN) * p_light
    return Color.from_hls(hue, light, sat).hex


def main():  # noqa

    # exclude Puerto Rico
    geojson_path_original = os.path.join(
        "examples_data", "geojson_data", "us-states.geo.json"
    )
    gdf = gpd.read_file(geojson_path_original)
    gdf = gdf[gdf["NAME"] != "Puerto Rico"]
    geojson_path = os.path.join(
        os.path.dirname(__file__),
        "us-states-1.geo.json",
    )
    gdf.to_file(geojson_path, driver="GeoJSON")

    values = []
    colors = []
    labels = []
    group_label_to_group = {"state": {}}
    info_idx = get_info_idx()
    state_to_code = get_state_to_code()
    for __, row in gdf.iterrows():
        state = row["NAME"]
        label = state_to_code[state]
        labels.append(label)
        info = info_idx.get(state)
        electoral_votes = int(round(info["EVs"]))

        if state == "Maine":
            electoral_votes = 4
        if state == "Nebraska":
            electoral_votes = 5

        values.append(electoral_votes)
        color = get_color(info)

        # color = Color.random()
        colors.append(color)

        group_label_to_group["state"][label] = label

    algo = DCN1985.from_geojson(
        geojson_path=geojson_path,
        values=values,
        algo_params=DCN1985AlgoParams(
            max_iterations=10,
        ),
    )

    __, dcn_list = algo.build(os.path.dirname(__file__))

    polygons = dcn_list[-1].polygons

    values = dcn_list[-1].values
    total_values = sum(values)
    log.debug(f"{total_values=}")
    hexbin_path = os.path.join(
        os.path.dirname(__file__),
        "hexbin.svg",
    )

    def post_process(data):  # noqa: CFQ001
        idx = data["idx"]

        def get_pos(a_ia):
            a, ia = a_ia
            return idx[a][ia - 1]

        def set_pos(a_ia, pos):
            a, ia = a_ia
            idx[a][ia - 1] = pos

        def swap(*a_ia_list):
            t = get_pos(a_ia_list[0])
            for i in range(len(a_ia_list) - 1):
                set_pos(a_ia_list[i], get_pos(a_ia_list[i + 1]))
            set_pos(a_ia_list[-1], t)

        def add(pos1, pos2):
            return (pos1[0] + pos2[0], pos1[1] + pos2[1])

        def sub(pos1, pos2):
            return (pos1[0] - pos2[0], pos1[1] - pos2[1])

        def move_rel(a_ia, b_ib, dx_dy):
            set_pos(a_ia, add(get_pos(b_ib), dx_dy))

        def move_all_rel(a, b_ib, dx_dy):
            dx_dy1_list = []
            for pos in idx[a]:
                dx_dy1 = sub(pos, get_pos((a, 1)))
                dx_dy1_list.append(dx_dy1)

            for ia, dx_dy1 in enumerate(dx_dy1_list, start=1):
                move_rel((a, ia), b_ib, add(dx_dy, dx_dy1))

        # EAST
        swap(("CT", 1), ("NY", 28))
        swap(("MD", 9), ("DE", 1))
        swap(("MD", 10), ("DE", 2))

        swap(("PA", 19), ("NJ", 2))
        swap(("PA", 7), ("NY", 17))

        swap(("RI", 1), ("MA", 11))
        move_rel(("ME", 4), ("ME", 2), (0, -1))

        # NORTH
        move_rel(
            ("MT", 1),
            ("WY", 1),
            (0, -1),
        )
        move_rel(
            ("ID", 1),
            ("ID", 3),
            (0, -1),
        )

        # WEST
        swap(("NV", 6), ("UT", 2))
        swap(("UT", 2), ("AZ", 1), ("CA", 28))
        swap(("UT", 3), ("NV", 6))
        swap(("AZ", 1), ("CA", 45))

        swap(("NV", 1), ("CA", 28))
        swap(("NV", 4), ("CA", 15))
        swap(("NV", 2), ("CA", 45))

        swap(("NM", 1), ("AZ", 6))
        swap(("NM", 5), ("TX", 1))

        # SOUTH
        swap(("AR", 1), ("OK", 7))

        # Hawaii
        move_all_rel("HI", ("CA", 50), (0, 2))

        # Alaska
        move_rel(
            ("AK", 2),
            ("AK", 1),
            (0, -1),
        )
        move_rel(
            ("AK", 3),
            ("AK", 1),
            (-1, -0.5),
        )

        move_all_rel("AK", ("MT", 4), (0, -2))

        data["idx"] = idx
        return data

    custom_color_map = {}
    for state, a_ia in [
        ["Maine’s 1st District", ("ME", 3)],
        ["Maine’s 2nd District", ("ME", 4)],
        ["Nebraska’s 1st District", ("NE", 2)],
        ["Nebraska’s 2nd District", ("NE", 3)],
        ["Nebraska’s 3rd District", ("NE", 4)],
    ]:
        info = info_idx[state]
        color = get_color(info)
        custom_color_map[a_ia] = color

    mid_x = 45.5
    mid_y = 20.784609690826528
    rendered_svg_custom = [
        _(
            "text",
            "2024 US Presidential Election",
            dict(
                x=mid_x,
                y=9.5,
                fill="black",
                font_size=0.7,
                text_anchor="middle",
                dominant_baseline="middle",
            ),
        ),
    ]

    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=total_values,
        custom_color_map=custom_color_map,
        rendered_svg_custom=rendered_svg_custom,
    ).write(
        hexbin_path=hexbin_path,
        post_process=post_process,
    )


if __name__ == "__main__":
    main()