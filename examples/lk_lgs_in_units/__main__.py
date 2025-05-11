def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import (
        DCN1985,
        DCN1985AlgoParams,
        DCN1985RenderParams,
        HexBinRenderer,
    )
    from utils import Log

    log = Log("lk_lgs_in_units")

    def get_random_color_hex():
        import random

        def random_color():
            return "#{:06x}80".format(random.randint(0, 0xFFFFFF))

        return random_color()

    ents = Ent.list_from_type(EntType.LG)
    log.debug(f"Found {len(ents)} LGs")
    group_label_to_group = {
        "District": {},
        "Province": {},
    }
    values = []
    colors = []
    district_to_color = {}
    for ent in ents:
        values.append(1)
        label = ent.name
        district_id = ent.district_id
        group_label_to_group["District"][label] = district_id
        group_label_to_group["Province"][label] = ent.province_id
        if district_id not in district_to_color:
            district_to_color[district_id] = get_random_color_hex()
        color = district_to_color[district_id]
        colors.append(color)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=False,
            max_iterations=40,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Units",
        ),
    )
    _, dcn_list = algo.build(os.path.dirname(__file__))
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values

    def post_process(data):  # noqa: CFQ001

        idx = data["idx"]

        def move(a, d):
            dx, dy = d
            idx[a][0] = [idx[a][0][0] + dx, idx[a][0][1] + dy]

        def swap(a, b):
            idx[a][0], idx[b][0] = idx[b][0], idx[a][0]

        # Kandy & Badulla
        swap("Minipe PS", "Rideemaliyadda PS")
        swap("Udadumbara PS", "Mahiyanganaya PS")
        swap("Minipe PS", "Mahiyanganaya PS")

        # Hambantota & Moonaragala
        swap("Tissamaharama PS", "Thanamalvila PS")

        # Jaffna
        move("Delft PS", (1, -0.5))

        # Mannar
        move("Musali PS", (0, -1))

        # Vavuniya & Mullaitivu
        swap("Vavuniya North PS", "Manthai East PS")

        # Mullaitivu & Trincomalee
        swap("Padavi Sri Pura PS", "Padaviya PS")

        # Trincomalee & Polonnaruwa
        swap("Kanthalai PS", "Hingurakgoda PS")

        # Polonnaruwa & Batticaloa
        swap("Dimbulagala PS", "Koralai Pattu West PS")

        # Ampara & Moneragala
        swap("Namaloya PS", "Bibile PS")
        swap("Ampara UC", "Madulla PS")

        swap("Irakkamam PS", "Bibile PS")
        swap("Sammanthurai PS", "Madulla PS")

        swap("Damana PS", "Bibile PS")
        swap("Akkaraipattu PS", "Madulla PS")

        # Kurunegala & Puttalam
        swap("Giribawa PS", "Karuwalagaswewa PS")

        # Puttalam
        move("Arachchikattuwa PS", (0, -1))
        move("Chilaw UC", (1, -0.5))

        # Badulla & Moneragala
        swap("Passara PS", "Medagama PS")

        # -----------------------------------
        # VALIDATE

        has_error = False
        for a, data_a in idx.items():
            pa = f"{data_a[0][0]:.1f},{data_a[0][1]:.1f}"
            for b, data_b in idx.items():
                pb = f"{data_b[0][0]:.1f},{data_b[0][1]:.1f}"
                if a == b:
                    continue
                if pa == pb:
                    log.error(f"Overlap {a} == {b} ({pb})")
                    has_error = True

        if has_error:
            raise Exception("Overlapping Polygons found")

        return data

    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=len(ents),
    ).write(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process,
    )


if __name__ == "__main__":
    main()
