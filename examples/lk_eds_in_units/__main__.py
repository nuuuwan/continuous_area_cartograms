def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, HexBin

    ents = Ent.list_from_type(EntType.ED)

    values = []
    for _ in ents:
        values.append(1)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=30,
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

    HexBin(polygons, labels, total_value=22).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.png",
        ),
    )


if __name__ == "__main__":
    main()
