def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    ents = Ent.list_from_type(EntType.DSD)
    ents = [ent for ent in ents if ent.province_id in ["LK-5"]]
    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            preprocess_tolerance=0.0,
        ),
        render_params=DCN1985RenderParams(
            super_title="Eastern Province (Sri Lanka)'s DSDs",
            title="Population",
        ),
    )
    algo.build(os.path.dirname(__file__))


if __name__ == "__main__":
    main()
