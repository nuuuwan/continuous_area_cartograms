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
            if k not in ["electors", "polled", "valid", "rejected"]:
                return k
        raise ValueError("No winning party found")

    ents = Ent.list_from_type(EntType.PROVINCE)
    group_to_label_to_group = {"Default": {}}
    values = []
    colors = []

    Ent.from_id("LK")

    for ent in ents:
        values.append(1)
        label = ent.name
        group = {
            "LK-4": "G1",
            "LK-6": "G2",
            "LK-7": "G2",
            "LK-1": "G3",
            "LK-2": "G3",
            "LK-5": "G3",
            "LK-3": "G4",
            "LK-8": "G4",
            "LK-9": "G4",
        }[ent.id]
        group_to_label_to_group["Default"][label] = group

        gig_table_prespoll = GIGTable(
            "government-elections-presidential", "regions-ec", "2015"
        )

        winning_party = get_winning_party(ent.gig(gig_table_prespoll))
        if winning_party == "NDF":
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
        idx = data["idx"]

        idx["Northern"] = [[0.0, 0.5]]
        idx["Southern"] = [[0.0, 3.5]]

        data["idx"] = idx
        return data

    HexBinRenderer(
        polygons,
        labels,
        group_to_label_to_group,
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
