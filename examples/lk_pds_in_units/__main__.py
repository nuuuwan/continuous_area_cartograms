def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985RenderParams

    ents = Ent.list_from_type(EntType.PD)
    values = [1 for _ in ents]
    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Units",
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        )
    )


if __name__ == "__main__":
    main()
