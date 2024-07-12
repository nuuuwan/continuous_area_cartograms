def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985RenderParams, HexBin

    ents = Ent.list_from_type(EntType.PROVINCE)

    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            title="Sri Lanka's Provinces",
            start_value_unit="km2",
            end_value_unit="Population",
            start_total_value=65_610,
        ),
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
