def main():
    import os

    from gig import Ent, EntType

    from cac import DCN1985, HexBin

    ents = Ent.list_from_type(EntType.DISTRICT)

    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(
        ents,
        values,
        max_iterations=10,
        title="Sri Lanka's Districts",
        area_unit="km2",
        value_unit="Population",
        true_total_area=65_610,
    )
    polygons = algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        ),
    )

    HexBin(polygons).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            'output',
            'hexbin.png',
        )
    )


if __name__ == "__main__":
    main()
