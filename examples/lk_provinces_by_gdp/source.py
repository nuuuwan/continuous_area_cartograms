def main():
    import os

    from gig import Ent, EntType

    from cac import DCN1985, HexBin

    ents = Ent.list_from_type(EntType.PROVINCE)

    # Source: https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/press/pr/press_pgdp_2022_e.pdf
    GDP_DATA_IDX = {
        'LK-1': 7_494_822,
        'LK-2': 1_823_459 ,
        'LK-3': 1_614_660,
        'LK-4': 752_276,
        'LK-5': 963_957 ,
        'LK-6': 1_955_294,
        'LK-7': 878_248,
        'LK-8': 848_092 ,
        'LK-9': 1_269_383 ,
    }

    values = []
    for ent in ents:
        values.append(GDP_DATA_IDX[ent.id])

    algo = DCN1985.from_ents(
        ents,
        values,
        title="Sri Lanka's Provinces",
        area_unit="km2",
        value_unit="GDP (LKR M)",
        true_total_area=65_610,
    )
    polygons = algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        ),
    )

    HexBin(polygons).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            'output',
            'hexbin.png',
        )
    )


if __name__ == "__main__":
    main()
