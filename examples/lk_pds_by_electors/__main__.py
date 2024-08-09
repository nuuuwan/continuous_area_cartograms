def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import (DCN1985, DCN1985AlgoParams, DCN1985RenderParams,
                     HexBinRenderer)

    gig_table_last_election = GIGTable(
        "government-elections-parliamentary", "regions-ec", "2020"
    )
    ents = Ent.list_from_type(EntType.PD)

    values = []
    label_to_group = {}
    colors = []
    for ent in ents:
        gig_table_row = ent.gig(gig_table_last_election)
        values.append(gig_table_row.electors)

        label = ent.name
        group = label
        label_to_group[label] = group
        color = "#8008"
        colors.append(color)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=30,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Registered Voter Pop.",
        ),
    )
    _, dcn_list = algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values
    HexBinRenderer(
        polygons, labels, label_to_group, colors, values, total_value=220
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
    )


if __name__ == "__main__":
    main()
