def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import (DCN1985, DCN1985AlgoParams, DCN1985RenderParams,
                     HexBinRenderer)

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

    for ent in ents:
        values.append(1)
        label = ent.name
        group = ent.district_id
        label_to_group[label] = group

        gig_table_prespoll = GIGTable(
            "government-elections-presidential", "regions-ec", "2015"
        )

        winning_party = get_winning_party(ent.gig(gig_table_prespoll))
        if winning_party == 'NDF':
            color = "#080"
        else:
            color = "#00c"

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

        # North-Western
        idx['Chilaw'][0] = [2.0, 8.5]
        idx['Nattandiya'][0] = [2.0, 9.5]

        # Central
        idx['Walapane'][0] = [10.0, 13.5]

        # # Uva
        idx['Bibile'][0] = [12.0, 14.5]
        idx['Monaragala'][0] = [12.0, 15.5]

        idx['Mahiyanganaya'][0] = [11.0,12.0]
        idx['Viyaluwa'][0] = [10.0,12.5]
        idx['Uva Paranagama'][0] = [11.0, 13.0]

        # Eastern
        idx['Batticaloa'][0] = [10.0,9.5]
        idx['Paddiruppu'][0] = [11.0,10.0]

        idx['Ampara'][0] = [11.0, 11.0]
        idx['Samanthurai'][0] = [12.0,11.5]
        idx['Kalmunai'][0] = [12.0,12.5]
        idx['Pothuvil'][0] = [13.0,13.0]

        idx['Trincomalee'][0] = [9.0, 6.0]
        idx['Seruvila'][0] = [9, 7]
        idx['Muttur'][0] = [10.0, 7.5]

        # Southern
        idx['Balapitiya'][0] = [2.0, 18.5]
        idx['Ambalangoda'][0] = [3.0, 18]

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
