def main():
    import os

    from gig import Ent, EntType

    from cac import DCN1985

    ents = Ent.list_from_type(EntType.DISTRICT)
    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(ents, values)
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
