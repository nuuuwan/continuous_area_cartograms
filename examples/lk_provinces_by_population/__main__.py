def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985RenderParams, HexBinRenderer

    ents = Ent.list_from_type(EntType.PROVINCE)

    values = []
    label_to_group = {}
    colors = []
    for ent in ents:
        values.append(ent.population)
        label = ent.name
        label_to_group[label] = ent.name
        colors.append("red")

    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Provinces",
            title="Population",
        ),
    )
    _, dcn_list = algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels

    HexBinRenderer(
        polygons, labels, label_to_group, colors, total_value=22
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
    )


if __name__ == "__main__":
    main()
