### [Build From Polygons](examples/build_from_polygons)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_polygons">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_polygons/output/animated.gif" height="240px" />
  </a>

</p>

```python
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
    )

    new_polygon = dnc.run(
        dir_output=os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

    print(new_polygon)

    # [<POLYGON ((0.032 0.232, 0.142 0.979, 0.68 1.32, 0.587 0.078, 0.032 0.232))>, <POLYGON ((0.587 0.078, 0.68 1.32, 1.922 1.413, 2.122 -0.122, 0.587 0.078))>, <POLYGON ((0.142 0.979, 0.112 1.888, 1.021 1.858, 0.68 1.32, 0.142 0.979))>, <POLYGON ((0.68 1.32, 1.021 1.858, 1.768 1.968, 1.922 1.413, 0.68 1.32))>]

```
