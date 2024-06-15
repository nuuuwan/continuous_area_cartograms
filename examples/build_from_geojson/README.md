### [Build From Geojson](examples/build_from_geojson)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_geojson">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_geojson/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from cac import DCN1985

    algo = DCN1985.from_geojson(
        geojson_path=os.path.join(
            os.path.dirname(__file__), 'geojson_data', 'Provinces.geo.json'
        ),
        values=[1, 1, 3, 1, 1, 1, 1, 1, 1],  # LK-11 - Western Province
    )

    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
