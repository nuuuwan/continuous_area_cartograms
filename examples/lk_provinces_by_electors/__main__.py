import os

from gig import Ent, EntType, GIGTable

from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, HexBinRenderer


def main():  # noqa
    gig_table_elec_parl_2020 = GIGTable(
        "government-elections-parliamentary", "regions-ec", "2020"
    )
    gig_table_elec_pres_2019 = GIGTable(
        "government-elections-presidential", "regions-ec", "2019"
    )
    gig_table_elec_parl_2015 = GIGTable(
        "government-elections-presidential", "regions-ec", "2015"
    )
    ents = Ent.list_from_type(EntType.PROVINCE)

    values = []
    group_label_to_group = {
        'Province': {},
    }
    colors = []

    total_electors = 0
    min_electors = None
    for ent in ents:
        row2020 = ent.gig(gig_table_elec_parl_2020)
        electors = row2020.electors
        total_electors += electors
        if min_electors is None or electors < min_electors:
            min_electors = electors

    budgeted_total_value = (total_electors / min_electors) * 0.501
    total_value = 0
    used_ents = []
    for ent in ents:
        row2020 = ent.gig(gig_table_elec_parl_2020)
        f_value = row2020.electors * budgeted_total_value / total_electors
        value = int(round(f_value, 0))
        if value == 0:
            print(f"Skipping {ent.name} ({f_value:.2f}) due to zero value")
            continue
        print(
            f'{value} ({f_value:.2f})'.ljust(10),
            ent.name,
        )
        used_ents.append(ent)
        values.append(value)
        total_value += value
        label = ent.name

        group_label_to_group['Province'][label] = ent.province_id

        # color
        row2019 = ent.gig(gig_table_elec_pres_2019)
        row2015 = ent.gig(gig_table_elec_parl_2015)

        blue2019 = row2019.SLPP > row2019.NDF
        blue2015 = row2015.UPFA > row2015.NDF
        if blue2019 and blue2015:
            color = "#8008"
        elif blue2019:
            color = "#f808"
        else:
            color = "#0c08"
        colors.append(color)

    print(f'{budgeted_total_value=:.2f}, {total_value=}')

    algo = DCN1985.from_ents(
        used_ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=100,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Registered Voter Pop.",
        ),
    )
    _, dcn_list = algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

    def post_process(data):
        idx = data['idx']

        def swap(a, b):
            idx[a], idx[b] = idx[b], idx[a]

        idx['Uva'] = idx['Eastern']
        idx['Eastern'] = [[2, 1]]
        data['idx'] = idx
        return data

    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values
    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=total_value,
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process=post_process,
    )


if __name__ == "__main__":
    main()
