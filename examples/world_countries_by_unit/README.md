# World Countries By Unit

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/world_countries_by_unit/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    import geopandas

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf_world = gdf_world[gdf_world['continent'] != 'Antarctica']

    values = [1 for _ in gdf_world['pop_est'].tolist()]
    algo = DCN1985.from_gdf(
        gdf_world,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=True,
        ),
        render_params=DCN1985RenderParams(
            super_title="World",
            title="Unit",
        ),
    )
    algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

if __name__ == "__main__":
    main()

```
