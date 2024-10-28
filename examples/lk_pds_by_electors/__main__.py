import os
import random

from gig import Ent, EntType, GIGTable

from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, HexBinRenderer


def get_random_color():
    h = random.randint(0, 240)
    s = 100
    light = random.choice([25, 50, 75])
    a = 0.75
    return f"hsla({h}, {s}%, {light}%, {a})"


def main():  # noqa
    gig_table_elec_parl_2020 = GIGTable(
        "government-elections-parliamentary", "regions-ec", "2020"
    )
    gig_table_elec_pres_2019 = GIGTable(
        "government-elections-presidential", "regions-ec", "2019"
    )
    gig_table_elec_parl_2015 = GIGTable(
        "government-elections-presidential", "regions-ec", "2015"
    )
    ents = Ent.list_from_type(EntType.PD)

    values = []
    group_label_to_group = {
        "PD": {},
        "ED": {},
        "Province": {},
    }
    colors = []

    total_electors = 0
    min_electors = None
    for ent in ents:
        row2020 = ent.gig(gig_table_elec_parl_2020)
        electors = row2020.electors
        total_electors += electors
        if min_electors is None or electors < min_electors:
            min_electors = electors

    budgeted_total_value = (total_electors / min_electors) * 0.501
    total_value = 0
    used_ents = []
    for ent in ents:
        row2020 = ent.gig(gig_table_elec_parl_2020)
        f_value = row2020.electors * budgeted_total_value / total_electors
        value = int(round(f_value, 0))
        if value == 0:
            print(f"Skipping {ent.name} ({f_value:.2f}) due to zero value")
            continue
        print(
            f"{value} ({f_value:.2f})".ljust(10),
            ent.name,
        )
        used_ents.append(ent)
        values.append(value)
        total_value += value
        label = ent.name

        group_label_to_group["PD"][label] = ent.name
        group_label_to_group["ED"][label] = ent.ed_id
        group_label_to_group["Province"][label] = ent.province_id

        # color
        row2019 = ent.gig(gig_table_elec_pres_2019)
        row2015 = ent.gig(gig_table_elec_parl_2015)

        blue2019 = row2019.SLPP > row2019.NDF
        blue2015 = row2015.UPFA > row2015.NDF
        if blue2019 and blue2015:
            color = "#8008"
        elif blue2019:
            color = "#f808"
        else:
            color = "#0c08"
        colors.append(get_random_color())

    print(f"{budgeted_total_value=:.2f}, {total_value=}")

    algo = DCN1985.from_ents(
        used_ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
            max_iterations=40,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Registered Voter Pop.",
        ),
    )
    _, dcn_list = algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

    def post_process(data):
        idx = data["idx"]

        def swap(a, b):
            idx[a], idx[b] = idx[b], idx[a]

        def swap_i(a, i, b, j):
            idx[a][i], idx[b][j] = idx[b][j], idx[a][i]

        def move(a, dx, dy):
            idx[a] = [(x + dx, y + dy) for x, y in idx[a]]

        # EC-04
        swap_i("Teldeniya", 0, "Kundasale", -1)

        # EC-05
        idx["Rattota"][-1] = idx["Laggala"][0]
        idx["Laggala"][0] = [14, 15.5]

        # EC-09
        idx["Tangalle"][-1] = [15.0, 27.0]
        idx["Tangalle"][1] = [16.0, 27.5]
        move("Thissamaharama", 0, -1)

        # EC-10
        move("Kilinochchi", 0, 4)
        for pd_name in [
            "Vaddukoddai",
            "Kankesanthurai",
            "Manipay",
            "Kopay",
            "Udupiddy",
            "Point Pedro",
            "Chavakachcheri",
            "Nallur",
            "Jaffna",
        ]:
            move(pd_name, 2, 5)
        idx["Kayts"] = [[6.0, 6.5]]

        # EC-11
        idx["Vavuniya"] = [[9.0, 10.0], [10.0, 10.5], [11.0, 10]]
        idx["Mannar"] = [[7.0, 10.0], [8.0, 9.5]]
        move("Mullaitivu", 0, 3)

        # EC-12
        idx["Kalkudah"][-1] = [16.0, 15.5]
        idx["Kalkudah"][0] = [17.0, 15.0]
        move("Batticaloa", -1, -0.5)
        idx["Paddiruppu"][0] = [18.0, 17.5]

        # EC-13
        idx["Pothuvil"][-1] = [19.0, 24.0]
        idx["Ampara"][0] = [16.0, 17.5]
        move("Samanthurai", -1, 0.5)
        idx["Kalmunai"] = [[19.0, 19.0], [20.0, 19.5]]

        # EC-14
        idx["Muttur"] = [[18.0, 14.5], [17, 14]]
        idx["Seruvila"] = [[14.0, 11.5], [15.0, 12.0]]

        idx["Trincomalee"] = [[17.0, 13.0], [16.0, 12.5]]

        # EC-17
        idx["Kekirawa"][0] = [13.0, 12.0]
        move("Horowpothana", 1, 0.5)
        idx["Horowpothana"][0] = [12, 11.5]
        idx["Mihinthale"] = [[11.0, 12.0]]
        idx["Anuradhapura East"][-1] = [10.0, 11.5]
        move("Medawachchiya", 1, 1.5)

        # EC-18
        idx["Polonnaruwa"][-1] = [15.0, 15.0]
        idx["Polonnaruwa"][0] = [16.0, 13.5]
        idx["Medirigiriya"][-1] = [15.0, 13.0]
        idx["Medirigiriya"][0] = [14.0, 12.5]
        idx["Minneriya"][0] = [14.0, 13.5]

        # EC-19
        idx["Mahiyanganaya"][0] = idx["Viyaluwa"][0]
        idx["Viyaluwa"] = [[18, 20.5]]

        # EC-20
        idx["Wellawaya"][-1] = [18, 24.5]
        idx["Monaragala"][0] = [18, 23.5]
        idx["Bibile"][0] = [19, 22]

        # EC-21
        idx["Kolonna"][-1] = [15.0, 26.0]

        data["idx"] = idx
        return data

    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values
    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=total_value,
    ).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process=post_process,
    )


if __name__ == "__main__":
    main()
