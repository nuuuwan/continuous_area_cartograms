### [World Countries By Population](examples/world_countries_by_population)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/world_countries_by_population">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/world_countries_by_population/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    import geopandas

    from cac import DCN1985

    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf_world = gdf_world[gdf_world['continent'] != 'Antarctica']

    values = gdf_world['pop_est'].tolist()
    algo = DCN1985.from_gdf(
        gdf_world,
        values,
        do_shrink=True,
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
