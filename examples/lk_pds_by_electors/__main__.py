import os
from gig import Ent, EntType, GIGTable
from cac import (DCN1985, DCN1985AlgoParams, DCN1985RenderParams,
                    HexBinRenderer)

   
def main():  # noqa
    gig_table_last_election = GIGTable(
        "government-elections-parliamentary", "regions-ec", "2020"
    )
    ents = Ent.list_from_type(EntType.PD)

    values = []
    label_to_group = {}
    colors = []

    total_electors = 0
    min_electors = None
    for ent in ents:
        gig_table_row = ent.gig(gig_table_last_election)
        electors = gig_table_row.electors
        total_electors += electors
        if min_electors is None or electors < min_electors:
            min_electors = electors

    budgeted_total_value = int((total_electors / min_electors) / 2) + 1
    total_value = 0
    used_ents = []
    for ent in ents:
        gig_table_row = ent.gig(gig_table_last_election)
        f_value = gig_table_row.electors * budgeted_total_value / total_electors
        value = int(round(f_value, 0))
        if value == 0:
            print(f"Skipping {ent.name} ({f_value:.2f}) due to zero value")
            continue
        used_ents.append(ent)
        values.append(value)
        total_value += value
        label = ent.name
        group = label
        label_to_group[label] = group
        color = "#8008"
        colors.append(color)

    print(f'{budgeted_total_value=}, {total_value=}')

    algo = DCN1985.from_ents(
        used_ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=30,
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
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values
    HexBinRenderer(
        polygons, labels, label_to_group, colors, values, total_value=total_value
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process=None,
    )


if __name__ == "__main__":
    main()
