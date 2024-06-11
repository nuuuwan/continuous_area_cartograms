def main():
    import os

    from gig import Ent, EntType

    from cac import DNC

    ents = Ent.list_from_type(EntType.DISTRICT)
    values = []
    for ent in ents:
        values.append(ent.population)

    dnc = DNC.from_ents(ents, values)
    dir_output = os.path.join(
        'example_images',
        os.path.basename(__file__)[:-3],
    )
    dnc.run(dir_output)


if __name__ == "__main__":
    main()
