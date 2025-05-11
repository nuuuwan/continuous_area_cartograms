def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import (
        DCN1985,
        DCN1985AlgoParams,
        DCN1985RenderParams,
        HexBinRenderer,
    )
    from utils import Log
    from utils_future import Color

    log = Log("lk_lgs_in_units")

    ents = Ent.list_from_type(EntType.LG)
    log.debug(f"Found {len(ents)} LGs")
    group_label_to_group = {
        "District": {},
        "Province": {},
    }
    values = []
    colors = []
    id_to_color = {}
    for ent in ents:
        values.append(1)
        label = ent.name
        district_id = ent.district_id
        province_id = ent.province_id

        group_label_to_group["District"][label] = district_id
        group_label_to_group["Province"][label] = province_id

        color_id = district_id
        if color_id not in id_to_color:
            id_to_color[color_id] = Color.random()
        color = id_to_color[color_id]
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

        def multi_swap(*a_list):
            for a, b in zip(a_list[::2], a_list[1::2]):
                idx[a][0], idx[b][0] = idx[b][0], idx[a][0]

        def swap(a, b):
            multi_swap(a, b)

        # Kandy & Badulla
        swap("Minipe PS", "Rideemaliyadda PS")
        swap("Udadumbara PS", "Mahiyangana PS")
        swap("Minipe PS", "Mahiyangana PS")

        # Hambantota & Moonaragala
        swap("Thissamaharama PS", "Thanamalwila PS")

        # Jaffna
        move("Delft PS", (1, -0.5))

        # Mannar
        move("Musali PS", (0, -1))

        # Vavuniya & Mullaitivu
        swap("Vavuniya North PS", "Manthai East PS")

        # Mullaitivu & Trincomalee
        swap("Padavi Sri Pura PS", "Padaviya PS")

        # Trincomalee
        move("Muttur PS", (0, 1))
        move("Seruwila PS", (0, 1))
        move("Verugal PS", (1, 0.5))

        # Trincomalee & Polonnaruwa
        swap("Kanthale PS", "Medirigiriya PS")

        # Polonnaruwa & Batticaloa
        swap("Dimbulagala PS", "Koralai Pattu West PS")

        # Ampara & Moneragala
        swap("Namaloya PS", "Bibila PS")
        swap("Ampara UC", "Madulla PS")

        swap("Irakkamam PS", "Bibila PS")
        swap("Sammanthurai PS", "Madulla PS")

        swap("Damana PS", "Bibila PS")
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
