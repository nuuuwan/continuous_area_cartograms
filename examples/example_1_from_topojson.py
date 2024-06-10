def main():
    import os

    from cac import DNC

    id_to_value = {
        'LK-1': 3,
    }
    # The size of the other provinces default to 1

    dnc = DNC.from_topojson(
        topojson_path=os.path.join('example_data', 'Provinces.json'),
        get_ids=lambda gdf: gdf['prov_c'],
        id_to_value=id_to_value,
    )

    dnc.run(
        dir_output=os.path.join(
            'example_images',
            'example_1_from_topojson',
        )
    )


if __name__ == "__main__":
    main()
