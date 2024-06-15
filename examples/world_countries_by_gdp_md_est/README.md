<<<<<<< HEAD
### [World Countries By Gdp Md Est](examples/world_countries_by_gdp_md_est)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/world_countries_by_gdp_md_est">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/world_countries_by_gdp_md_est/output/animated.gif" height="240px" />
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

    values = gdf_world['gdp_md_est'].tolist()
    algo = DCN1985.from_gdf(
        gdf_world,
        values,
        min_log2_error=0.1,
        max_iterations=100,
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
=======
### [World Countries By Gdp Md Est](examples/world_countries_by_gdp_md_est)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/world_countries_by_gdp_md_est">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/world_countries_by_gdp_md_est/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    import geopandas

    from cac import DNC

    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf_world = gdf_world[gdf_world['continent'] != 'Antarctica']

    values = gdf_world['gdp_md_est'].tolist()
    dnc = DNC.from_gdf(
        gdf_world,
        values,
        do_shrink=True,
    )
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
>>>>>>> b61ab374069959fe6777f1645f6d362f98e25a94
