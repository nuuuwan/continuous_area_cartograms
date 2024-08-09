def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import (
        DCN1985,
        DCN1985AlgoParams,
        DCN1985RenderParams,
        HexBinRenderer,
    )

    def get_winning_party(row):
        for k in row.dict.keys():
            if k not in ['electors', 'polled', 'valid', 'rejected']:
                return k
        raise ValueError("No winning party found")

    ents = Ent.list_from_type(EntType.PD)
    label_to_group = {}
    values = []
    colors = []

    ent_lk = Ent.from_id('LK')
    YEARS = ['1982', '1988', '1994', '1999', '2005', '2010', '2015', '2019']

    for ent in ents:
        values.append(1)
        label = ent.name
        group = ent.ed_id
        label_to_group[label] = group

        n_matches = 0
        n_years = 0
        for year in YEARS[-1:]:
            n_years += 1
            gig_table_prespoll = GIGTable(
                "government-elections-presidential", "regions-ec", str(year)
            )

            winning_party = get_winning_party(ent.gig(gig_table_prespoll))
            winning_party_lk = get_winning_party(
                ent_lk.gig(gig_table_prespoll)
            )

            if winning_party == winning_party_lk:
                n_matches += 1

        p_matches = n_matches / n_years

        if p_matches > 0.5:
            hue = 0
            p = p_matches - 0.5
        else:
            hue = 240
            p = 0.5 - p_matches

        light = 40 + 50 * (1 - p)
        color = f'hsl({hue},75%,{light}%)'
        colors.append(color)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            # do_shrink=True,
            max_iterations=100,
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
    values = dcn_list[-1].values

    HexBinRenderer(
        polygons, labels, label_to_group, colors, values, total_value=len(ents)
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
    )


if __name__ == "__main__":
    main()
