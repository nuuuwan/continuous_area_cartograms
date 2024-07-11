def main():  # noqa
    import os

    from shapely import Polygon

    from cac import DCN1985

    def polygon_square(origin):
        return Polygon(
            [
                origin,
                (origin[0], origin[1] + 1),
                (origin[0] + 1, origin[1] + 1),
                (origin[0] + 1, origin[1]),
                origin,
            ]
        )

    def polygon_square_of_squares(n):
        polygons = []
        for i in range(n):
            for j in range(n):
                polygons.append(polygon_square((i, j)))
        return polygons

    polygons = polygon_square_of_squares(3)
    values = [100 for _ in range(len(polygons))]
    values[1] = 1
    values[3] = 1
    values[5] = 1
    values[7] = 1

    algo = DCN1985(
        polygons,
        values,
        max_iterations=20,
    )

    new_polygon = algo.run(
        dir_output=os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

    print(new_polygon)


if __name__ == "__main__":
    main()
