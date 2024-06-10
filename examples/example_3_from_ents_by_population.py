def main():
    import os

    from gig import Ent, EntType

    from cac import DNC

    ents = Ent.list_from_type(EntType.DISTRICT)
    id_to_value = {}
    for ent in ents:
        id_to_value[ent.id] = ent.population

    dnc = DNC.from_ents(ents, id_to_value)
    dir_output = os.path.join(
        'example_images',
        os.path.basename(__file__)[:-3],
    )
    dnc.run(dir_output)


if __name__ == "__main__":
    main()
