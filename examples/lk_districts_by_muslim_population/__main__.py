def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985, DCN1985RenderParams

    gig_table_last_election = GIGTable("population-religion", "regions", "2012")

    ents = [ent for ent in Ent.list_from_type(EntType.DISTRICT)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.islam)

    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Districts",
            title="Muslim Population",
        ),
    )
    algo.build(os.path.dirname(__file__))


if __name__ == "__main__":
    main()
