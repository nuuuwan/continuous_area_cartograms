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
        title="World",
        area_unit="km2",
        value_unit="Population",
        true_total_area=149_000_000,
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
