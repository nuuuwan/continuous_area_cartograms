### [Build From Topojson](examples/build_from_topojson)

<p align="center">

  <a href="build_from_topojson">
    <img src="build_from_topojson/output/animated.gif" height="320px" />
  </a>

</p>

```python
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'Provinces.json'
        ),
        values=[1, 1, 3, 1, 1, 1, 1, 1, 1],  # LK-11 - Western Province
    )

    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
