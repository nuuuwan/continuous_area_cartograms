# Africa By Gdp Md Est

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/africa_by_gdp_md_est/output/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    import geopandas

    from cac import DCN1985

    gdf = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf = gdf[gdf['continent'] == 'Africa']

    values = gdf['gdp_md_est'].tolist()
    algo = DCN1985.from_gdf(
        gdf,
        values,
        title="Africa",
        area_unit="km2",
        value_unit="GDP (USD M)",
        true_total_area=30_370_000,
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
