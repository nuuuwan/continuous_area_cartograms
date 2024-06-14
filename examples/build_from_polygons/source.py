def main():
    import os

    from shapely import Polygon

    from cac import DNC

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

    dnc = DNC(
        polygons,
        [1, 4, 1, 1],
        ['A', 'B', 'C', 'D'],
    )

    new_polygon = dnc.run(
        dir_output=os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

    print(new_polygon)

if __name__ == "__main__":
    main()
