def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    ents_all = Ent.list_from_type(EntType.DSD)

    IDX = {
        'LK-1127': 42,
        'LK-1103': 28,
        'LK-1124': 6,
        'LK-1109': 3,
        'LK-1136': 1,
        'LK-1133': 1,
        'LK-1121': 1,
    }

    ents = []
    values = []
    for ent in ents_all:
        value = IDX.get(ent.id)
        if value is None:
            continue
        ents.append(ent)
        values.append(value)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(do_shrink=True),
        render_params=DCN1985RenderParams(
            super_title="Colombo District's DSDs",
            title="SLASSCOM Members",
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        ),
    )


if __name__ == "__main__":
    main()
