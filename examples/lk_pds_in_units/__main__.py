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
        for year in YEARS:
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
            do_shrink=False,
            max_iterations=40,
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

    def post_process(data):
        idx = data['idx']

        # Central
        idx['Laggala'][0] = [9, 9]

        idx['Walapane'][0] = [10.0,12.5]
        idx['Hanguranketha'][0] = [10.0, 13.5]
        idx['Kothmale'][0] = [9, 14]
        idx['Nuwara Eliya Maskeliya'][0] = [8.0,14.5]

        # Northern
        for k in [
            'Chavakachcheri',
            'Jaffna',
            'Kankesanthurai',
            'Kopay',
            'Manipay',
            'Nallur',
            'Point Pedro',
            'Udupiddy',
            'Vaddukoddai',
        ]:
            idx[k][0][1] += 2
        idx['Kayts'][0] = [2, 3.5]

        # Eastern
        idx['Trincomalee'][0] = [9.0, 6.0]
        idx['Seruvila'][0] = [9.0, 7.0]
        idx['Muttur'][0] = [10.0,7.5]

        idx['Kalkudah'][0] = [11.0,8.0]
        idx['Batticaloa'][0] = [11.0, 9.0]
        idx['Paddiruppu'][0] = [10.0,9.5]

        idx['Ampara'][0] = [10.0,10.5]
        idx['Samanthurai'][0] = [11.0,10.0]
        idx['Kalmunai'][0] = [12.0,10.5]
        idx['Pothuvil'][0] = [12.0,11.5]

        # North-Western
        idx['Chilaw'][0] = [2.0, 8.5]
        idx['Nattandiya'][0] = [2.0, 9.5]

        # North-Central
        idx['Polonnaruwa'][0] = [10.0, 8.5]

        # Uva
        idx['Welimada'][0] = [9.0,15.0]
        idx['Bandarawela'][0] = [10.0, 15.5]
        idx['Uva Paranagama'][0] = [11.0, 12.0]

        idx['Hali Ela'][0] = [11.0,15.0]
        idx['Uva Paranagama'][0] = [10.0, 14.5]

        idx['Viyaluwa'][0] = [11.0,12]
        idx['Passara'][0] = [11.0, 13]

        idx['Bibile'][0] = [12.0,14.5]
        idx['Monaragala'][0] = [12.0, 15.5]

        data['idx'] = idx
        return data

    HexBinRenderer(
        polygons,
        labels,
        label_to_group,
        colors,
        values,
        total_value=len(ents),
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process,
    )


if __name__ == "__main__":
    main()
