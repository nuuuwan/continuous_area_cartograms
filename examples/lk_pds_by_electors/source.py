def main():
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985, HexBin

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = Ent.list_from_type(EntType.PD)

    values = []
    for ent in ents:
        gig_table_row = ent.gig(gig_table_last_election)
        values.append(gig_table_row.electors)

    algo = DCN1985.from_ents(
        ents,
        values,
        do_shrink=True,
        max_iterations=30,
        title="Sri Lanka's Polling Divisions",
        area_unit="km2",
        value_unit="Registered Voter Pop.",
        true_total_area=65_610,
    )
    polygons = algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

    HexBin(polygons, total_value=850).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            'output',
            'hexbin.png',
        ),
    )


if __name__ == "__main__":
    main()
