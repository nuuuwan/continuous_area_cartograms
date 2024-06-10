def main():
    import os

    from gig import Ent

    from cac import DNC

    id_to_value = {
        'LK-11': 3,
        'LK-12': 2,
        'LK-13': 1,
    }
    ents = Ent.list_from_id_list(id_to_value.keys())

    dnc = DNC.from_ents(ents, id_to_value)
    dnc.run(
        dir_output=os.path.join(
            'example_images',
            'example_2_from_ents',
        )
    )


if __name__ == "__main__":
    main()
