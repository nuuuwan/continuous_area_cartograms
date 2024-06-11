def main():
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join('example_data', 'Provinces.json'),
        values=[3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    )

    dnc.run(
        dir_output=os.path.join(
            'example_images',
            'example_1_from_topojson',
        )
    )


if __name__ == "__main__":
    main()
