def main():
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DNC

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = [ent for ent in Ent.list_from_type(EntType.PD)]
    id_to_value_num = {}
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        electors = row.electors
        id_to_value_num[ent.id] = electors

    total_electors = sum(id_to_value_num.values())
    id_to_value = {
        id: electors / total_electors
        for id, electors in id_to_value_num.items()
    }

    dnc = DNC.from_ents(ents, id_to_value)
    dir_output = os.path.join(
        'example_images',
        os.path.basename(__file__)[:-3],
    )
    dnc.run(
        dir_output=dir_output
    )


if __name__ == "__main__":
    main()
