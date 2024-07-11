def main():
    import os

    from gig import Ent, EntType

    from cac import DCN1985

    ents_all = Ent.list_from_type(EntType.DSD)

    IDX = {'LK-1127': 42, 'LK-1103': 28, 'LK-1124': 6, 'LK-1109': 3, 'LK-1136': 1, 'LK-1133': 1, 'LK-1121': 1}

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
        do_shrink=True,
        title="Colombo District's DSDs",
        area_unit="km2",
        value_unit="SLASSCOM Members",
        true_total_area=699,
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        ),
    )


if __name__ == "__main__":
    main()
