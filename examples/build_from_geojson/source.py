def main():
    import os

    from cac import DNC

    dnc = DNC.from_geojson(
        geojson_path=os.path.join(
            os.path.dirname(__file__), 'geojson_data', 'Provinces.geo.json'
        ),
        values=[1, 1, 3, 1, 1, 1, 1, 1, 1],  # LK-11 - Western Province
    )

    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
