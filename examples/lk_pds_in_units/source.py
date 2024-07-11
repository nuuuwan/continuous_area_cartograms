def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985

    ents = Ent.list_from_type(EntType.PD)
    values = [1 for _ in ents]
    algo = DCN1985.from_ents(
        ents,
        values,
        title="Sri Lanka's Polling Divisions",
        area_unit="km2",
        value_unit="Units",
        true_total_area=65_610,
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
