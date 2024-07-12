# Africa By Pop Est

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/africa_by_pop_est/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    import geopandas

    from cac import DCN1985, DCN1985RenderParams

    gdf = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf = gdf[gdf['continent'] == 'Africa']

    values = gdf['pop_est'].tolist()
    algo = DCN1985.from_gdf(
        gdf,
        values,
        render_params=DCN1985RenderParams(
            title="Africa",
            end_value_unit="Population",
            source_text="United Nations",
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

if __name__ == "__main__":
    main()

```
