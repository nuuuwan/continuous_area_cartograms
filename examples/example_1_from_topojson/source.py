def main():
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'Provinces.json'
        ),
        values=[3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    )

    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
