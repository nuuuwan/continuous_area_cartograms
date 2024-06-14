def main():
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DNC

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = [ent for ent in Ent.list_from_type(EntType.PD)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.electors)

    dnc = DNC.from_ents(ents, values, do_shrink=True)
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
