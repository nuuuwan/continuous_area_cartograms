def main():
    import os

    from gig import Ent, EntType

    from cac import DCN1985, HexBin

    ents = Ent.list_from_type(EntType.DISTRICT)
    ents = [ent for ent in ents if 'LK-4' in ent.id ]
    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(ents, values, max_iterations=10)
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
