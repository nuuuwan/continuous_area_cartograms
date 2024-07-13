from cac.extended import GridCAC

PARTY_TO_COLOR = {
    'JVP': 'red',
    'NDF': 'green',
    'NMPP': 'red',
    'PA': 'blue',
    'SLFP': 'blue',
    'SLMP': 'purple',
    'SLPP': 'maroon',
    'UNP': 'green',
    'UPFA': 'blue',
    'All Others': 'lightgrey',
    'Did not vote/Rejected': 'black',
}


def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    ents = Ent.list_from_type(EntType.ED)
    ent_lk = Ent.from_id('LK')

    dcn_list_list = []
    for year in [1982, 1988, 1994, 1999, 2005, 2010, 2015, 2019]:
        gig_table_last_election = GIGTable(
            'government-elections-presidential', 'regions-ec', f'{year}'
        )
        dcn_list = []

        gig_table_row_lk = ent_lk.gig(gig_table_last_election)
        dict_p_lk = gig_table_row_lk.dict_p
        parties = [
            k
            for k in list(dict_p_lk.keys())
            if k not in ['electors', 'polled', 'valid', 'rejected']
        ][:2] + ['All Others', 'Did not vote/Rejected']
        dict_lk = gig_table_row_lk.dict

        for i, party in enumerate(parties):
            values = []
            for ent in ents:
                gig_table_row = ent.gig(gig_table_last_election)
                if i == 3:
                    value = (
                        gig_table_row.dict['electors']
                        - gig_table_row.dict['valid']
                    )
                elif i == 2:
                    value = (
                        gig_table_row.dict['valid']
                        - gig_table_row.dict[parties[0]]
                        - gig_table_row.dict[parties[1]]
                    )
                else:
                    value = gig_table_row.dict[party]

                values.append(value)

            total_values = sum(values)
            if i == 0:
                total_values0 = total_values

            scale = total_values / total_values0

            if i != 3:
                p = total_values / dict_lk['valid']
                sub_title = f'{p:.0%}'
            else:
                p = total_values / dict_lk['valid']
                sub_title = f'{p:.0%} (of valid votes)'

            dnc = DCN1985.from_ents(
                ents,
                values,
                algo_params=DCN1985AlgoParams(
                    do_shrink=True,
                ),
                render_params=DCN1985RenderParams(
                    super_title=f"{year} Sri Lankan Presidential Election",
                    title=party,
                    sub_title=sub_title,
                    footer_text="Data Source: Election Commission of Sri Lanka",
                    end_value_color=PARTY_TO_COLOR.get(party, 'darkgrey'),
                    scale=scale,
                ),
            )
            dcn_list.append(dnc)
        dcn_list_list.append(dcn_list)

    GridCAC(dcn_list_list).build(
        os.path.join(
            os.path.dirname(__file__),
        ),
    )


if __name__ == "__main__":
    main()
