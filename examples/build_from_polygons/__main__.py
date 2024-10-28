def main():  # noqa
    import os

    from shapely import Polygon

    from cac import DCN1985

    polygons = [
        Polygon(
            [
                (0, 0),
                (0, 1),
                (1, 1),
                (1, 0),
                (0, 0),
            ]
        ),
        Polygon(
            [
                (1, 0),
                (1, 1),
                (2, 1),
                (2, 0),
                (1, 0),
            ]
        ),
        Polygon(
            [
                (0, 1),
                (0, 2),
                (1, 2),
                (1, 1),
                (0, 1),
            ]
        ),
        Polygon(
            [
                (1, 1),
                (1, 2),
                (2, 2),
                (2, 1),
                (1, 1),
            ]
        ),
    ]

    algo = DCN1985(
        polygons,
        [1, 4, 1, 1],
        ["A", "B", "C", "D"],
    )

    algo.build(dir_output=os.path.dirname(__file__))


if __name__ == "__main__":
    main()
