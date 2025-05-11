def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import (
        DCN1985,
        DCN1985AlgoParams,
        DCN1985RenderParams,
        HexBinRenderer,
    )
    from utils import Log

    log = Log("lk_lgs_in_units")

    def get_winning_party(row):
        for k in row.dict.keys():
            if k not in ["electors", "polled", "valid", "rejected"]:
                return k
        raise ValueError("No winning party found")

    ents = Ent.list_from_type(EntType.LG)
    log.debug(f"Found {len(ents)} LGs")
    group_label_to_group = {
        "District": {},
        "Province": {},
    }
    values = []
    colors = []

    for ent in ents:
        values.append(1)
        label = ent.name
        group_label_to_group["District"][label] = ent.district_id
        group_label_to_group["Province"][label] = ent.province_id

        gig_table_prespoll = GIGTable(
            "government-elections-presidential", "regions-ec", "2015"
        )

        winning_party = get_winning_party(ent.gig(gig_table_prespoll))
        if winning_party == "NDF":
            color = "#0808"
        else:
            color = "#00c8"

        colors.append(color)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=False,
            max_iterations=40,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Units",
        ),
    )
    _, dcn_list = algo.build(os.path.dirname(__file__))
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values

    def post_process(data):  # noqa: CFQ001
        return data

    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=len(ents),
    ).write(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process,
    )


if __name__ == "__main__":
    main()
