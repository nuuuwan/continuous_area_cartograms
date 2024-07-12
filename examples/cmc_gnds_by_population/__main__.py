def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    ents = Ent.list_from_type(EntType.GND)
    ents = [ent for ent in ents if ent.dsd_id in ['LK-1103', 'LK-1127']]
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
            super_title="Colombo MC's GNDs",
            title="Population",
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        )
    )


if __name__ == "__main__":
    main()
