def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985

    gig_table_last_election = GIGTable(
        'population-religion', 'regions', '2012'
    )

    ents = [ent for ent in Ent.list_from_type(EntType.DISTRICT)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.islam)

    algo = DCN1985.from_ents(
        ents,
        values,
        title="Sri Lanka's Districts",
        area_unit="km2",
        value_unit="Muslim Population",
        true_total_area=65_610,
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
