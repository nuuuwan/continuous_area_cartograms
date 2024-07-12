def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    ents_all = Ent.list_from_type(EntType.GND)

    IDX = {
        'LK-1103120': 10,
        'LK-1103170': 10,
        'LK-1127010': 8,
        'LK-1127005': 7,
        'LK-1127030': 5,
        'LK-1127065': 4,
        'LK-1127075': 4,
        'LK-1103140': 3,
        'LK-1127085': 3,
        'LK-1127045': 2,
        'LK-1127060': 2,
        'LK-1103175': 2,
        'LK-1127015': 2,
        'LK-1127050': 1,
        'LK-1127080': 1,
        'LK-1127070': 1,
        'LK-1103125': 1,
        'LK-1127090': 1,
        'LK-1103145': 1,
        'LK-1103135': 1,
        'LK-1127040': 1,
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
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            preprocess_tolerance=0.0,
        ),
        render_params=DCN1985RenderParams(
            title="Colombo MC's GNDs",
            start_value_unit="km2",
            end_value_unit="SLASSCOM Members",
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        ),
    )


if __name__ == "__main__":
    main()
