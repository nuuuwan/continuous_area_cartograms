def main():  # noqa
    import os

    from cac import DCN1985

    algo = DCN1985.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'DSDivisions.json'
        ),
    )

    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            
        )
    )


if __name__ == "__main__":
    main()
