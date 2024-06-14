### [Europe By Gdp Md Est](examples/europe_by_gdp_md_est)

<p align="center">

  <a href="europe_by_gdp_md_est">
    <img src="europe_by_gdp_md_est/output/animated.gif" height="320px" />
  </a>

</p>

```python
    import os

    import geopandas

    from cac import DNC

    gdf = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf = gdf[gdf['continent'] == 'Europe']
    gdf = gdf[gdf['name'] != 'Russia']

    values = gdf['gdp_md_est'].tolist()
    dnc = DNC.from_gdf(
        gdf,
        values,
    )
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
