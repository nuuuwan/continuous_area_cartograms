def main():  # noqa
    import os

    from cac import DCN1985

    algo = DCN1985.from_geojson(
        geojson_path=os.path.join(
            "examples_data", "geojson_data", "Provinces.geo.json"
        ),
        values=[1, 1, 3, 1, 1, 1, 1, 1, 1],  # LK-11 - Western Province
    )

    algo.build(os.path.dirname(__file__))


if __name__ == "__main__":
    main()
