def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import (DCN1985, DCN1985AlgoParams, DCN1985RenderParams,
                     HexBinRenderer)

    gig_table_last_election = GIGTable(
        "government-elections-presidential", "regions-ec", "2015"
    )

    ents = Ent.list_from_type(EntType.PD)
    label_to_group = {}
    values = []
    colors = []
    for ent in ents:
        values.append(1)
        label = ent.name
        group = ent.id[:-1]
        label_to_group[label] = group
        gig_table_row = ent.gig(gig_table_last_election)

        color = None
        winning_votes = None
        if gig_table_row.dict['UPFA'] > gig_table_row.dict['NDF']:
            color = '#028'
            winning_votes = gig_table_row.dict['UPFA']
        else:
            color = "#082"
            winning_votes = gig_table_row.dict['NDF']

        p_winning = winning_votes / gig_table_row.dict['valid']

        # convert to hex
        hex_alpha = hex(int((16 * p_winning)))[2:]
        color += hex_alpha
        colors.append(color)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=20,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Units",
        ),
    )
    _, dcn_list = algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels

    HexBinRenderer(
        polygons, labels, label_to_group, colors, total_value=160
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
    )


if __name__ == "__main__":
    main()
