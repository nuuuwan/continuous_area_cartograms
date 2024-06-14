def main():
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


if __name__ == "__main__":
    main()
