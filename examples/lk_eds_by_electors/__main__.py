def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, HexBin

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = Ent.list_from_type(EntType.ED)

    values = []
    for ent in ents:
        gig_table_row = ent.gig(gig_table_last_election)
        values.append(gig_table_row.electors)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=30,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Electoral Districts",
            title="Registered Voter Pop.",
        ),
    )
    _, dcn_list = algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )
    polygons = dcn_list[-1].polygons

    HexBin(polygons, total_value=225).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            'hexbin.png',
        ),
    )


if __name__ == "__main__":
    main()