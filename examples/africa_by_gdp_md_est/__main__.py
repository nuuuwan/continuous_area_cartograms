def main():  # noqa
    import os

    import geopandas

    from cac import DCN1985, DCN1985RenderParams

    gdf = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf = gdf[gdf['continent'] == 'Africa']

    values = gdf['gdp_md_est'].tolist()
    algo = DCN1985.from_gdf(
        gdf,
        values,
        render_params=DCN1985RenderParams(
            title="Africa",
            end_value_unit="GDP (USD M)",
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
