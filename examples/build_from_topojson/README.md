### [Build From Topojson](examples/build_from_topojson)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_topojson">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_topojson/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'DSDivisions.json'
        ),
    )

    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
