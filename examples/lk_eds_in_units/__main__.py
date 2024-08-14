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

    ents = Ent.list_from_type(EntType.ED)
    label_to_group = {}
    values = []
    colors = []

    Ent.from_id('LK')

    for ent in ents:
        values.append(1)
        label = ent.name
        group = ent.province_id
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
            super_title="Sri Lanka's Electoral Districts",
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

        for after, before in [
            ('Galle', 'Kalutara'),
            ('Kalutara', 'Colombo'),
            ('Colombo', 'Gampaha'),
            ('Gampaha', 'Kurunegala'),
            ('Kurunegala', 'Anuradhapura'),
            ('Anuradhapura', 'Vanni'),
            ('Vanni', 'Jaffna'),
            #
            ('Matara', 'Hambantota'),
            ('Hambantota', 'Moneragala'),
            ('Moneragala', 'Badulla'),
            ('Badulla', 'Digamadulla'),
            ('Digamadulla', 'Batticaloa'),
            ('Vanni', 'Jaffna'),
        ]:
            idx[after] = idx[before]

        idx['Jaffna'] = [[0.0, -0.5]]
        idx['Batticaloa'] = [[3.0, 1.0]]

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
