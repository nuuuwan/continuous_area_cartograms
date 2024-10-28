def main():  # noqa
    import os

    import geopandas

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    COUNTRY_TO_GOLD_MEDALS = {
        "Algeria": 2,
        "Argentina": 1,
        "Australia": 18,
        "Austria": 2,
        "Azerbaijan": 2,
        "Bahrain": 2,
        "Belgium": 3,
        "Botswana": 1,
        "Brazil": 3,
        "Bulgaria": 3,
        "Canada": 9,
        "Chile": 1,
        "China": 40,
        "Chinese Taipei": 2,
        "Croatia": 2,
        "Cuba": 2,
        "Czechia": 3,
        "Denmark": 2,
        "Dominica": 1,
        "Dominican Republic": 1,
        "Ecuador": 1,
        "Egypt": 1,
        "Ethiopia": 1,
        "France": 16,
        "Georgia": 3,
        "Great Britain": 14,
        "Greece": 1,
        "Guatemala": 1,
        "Hong Kong, China": 2,
        "Hungary": 6,
        "Indonesia": 2,
        "Iran": 3,
        "Ireland": 4,
        "Israel": 1,
        "Italy": 12,
        "Jamaica": 1,
        "Japan": 20,
        "Kazakhstan": 1,
        "Kenya": 4,
        "Morocco": 1,
        "Netherlands": 15,
        "New Zealand": 10,
        "Norway": 4,
        "Pakistan": 1,
        "Philippines": 2,
        "Poland": 1,
        "Portugal": 1,
        "Romania": 3,
        "Saint Lucia": 1,
        "Serbia": 3,
        "Slovenia": 2,
        "South Africa": 1,
        "South Korea": 13,
        "Spain": 5,
        "Sweden": 4,
        "Switzerland": 1,
        "Thailand": 1,
        "Tunisia": 1,
        "Uganda": 1,
        "Ukraine": 3,
        "United States": 40,
        "Uzbekistan": 8,
    }

    TRANSLATE_IDX = {
        "Taiwan": "Chinese Taipei",
        "Dominican Rep.": "Dominican Republic",
        "United Kingdom": "Great Britain",
        "United States of America": "United States",
    }

    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path("naturalearth_lowres")
    )
    gdf_world = gdf_world[gdf_world["continent"] != "Antarctica"]

    values = []
    used_countries = []
    country_list = gdf_world["name"].tolist()
    country_list_with_no_medals_data = []
    for country in country_list:
        country_k = country
        if TRANSLATE_IDX.get(country) is not None:
            country_k = TRANSLATE_IDX[country]

        if country_k in COUNTRY_TO_GOLD_MEDALS:
            values.append(COUNTRY_TO_GOLD_MEDALS[country_k])
            used_countries.append(country)
        else:
            country_list_with_no_medals_data.append(country)

    print("NO MEDALS DATA")
    for country in sorted(country_list_with_no_medals_data):
        print(f"    '{country}': None, ")

    print("NO GEO DATA")
    for country in sorted(
        set(COUNTRY_TO_GOLD_MEDALS.keys()) - set(used_countries)
    ):
        print(f"    None: '{country}', ")

    gdf_world = gdf_world[gdf_world["name"].isin(used_countries)]
    print(used_countries)
    print(values)

    algo = DCN1985.from_gdf(
        gdf_world,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
        ),
        render_params=DCN1985RenderParams(
            super_title="",
            title="2024 Summer Olympics - Gold Medals",
        ),
    )
    algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )


if __name__ == "__main__":
    main()
