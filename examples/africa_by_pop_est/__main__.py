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
            start_value_unit="km2",
            end_value_unit="Population",
            
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        )
    )


if __name__ == "__main__":
    main()
