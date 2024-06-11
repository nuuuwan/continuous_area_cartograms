def main():
    import os

    from gig import Ent

    from cac import DNC

    ents = Ent.list_from_id_list(['LK-11', 'LK-12', 'LK-13'])
    values = [3, 2, 1]
    dnc = DNC.from_ents(ents, values)
    dnc.run(
        os.path.join(
            'example_images',
            'example_2_from_ents',
        )
    )


if __name__ == "__main__":
    main()
