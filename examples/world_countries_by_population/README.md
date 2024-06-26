# World Countries By Population

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/world_countries_by_population/output/animated.gif" alt="alt" />
</p>

```python
def main():
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

if __name__ == "__main__":
    main()

```
