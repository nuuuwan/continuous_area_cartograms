def main():  # noqa
    import os

    from gig import EntType, GIGTable

    from cac import GIGTableMCAC

    GIGTableMCAC(
        GIGTable('population-ethnicity', 'regions', '2012'),
        EntType.DISTRICT,
    ).build(
        os.path.join(
            os.path.dirname(__file__),
            
        ),
    )


if __name__ == "__main__":
    main()
