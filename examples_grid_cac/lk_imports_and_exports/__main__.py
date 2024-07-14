def main():  # noqa
    import os

    import geopandas
    from utils import Log

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, GridCAC
    from examples_grid_cac.lk_imports_and_exports.lk_exports import lk_exports
    from examples_grid_cac.lk_imports_and_exports.lk_imports import lk_imports

    Log('main')

    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )

    names = []
    values_imports = []
    values_exports = []
    for name in gdf_world['name'].tolist():
        value_import = lk_imports.get(name, 0)
        value_export = lk_exports.get(name, 0)
        if value_import == 0 or value_export == 0:
            continue

        values_imports.append(value_import)
        values_exports.append(value_export)
        names.append(name)

    gdf_world = gdf_world[gdf_world['name'].isin(names)]

    algo_params = DCN1985AlgoParams(
        do_shrink=True,
    )
    dcn_list_list = [
        [
            DCN1985.from_gdf(
                gdf_world,
                values_imports,
                algo_params=algo_params,
                render_params=DCN1985RenderParams(
                    super_title="World",
                    title="Imports to Sri Lanka (USD M.)",
                    footer_text="Data Source: United Nations COMTRADE database (2023)",
                    end_value_color='red',
                ),
            )
        ],
        [
            DCN1985.from_gdf(
                gdf_world,
                values_exports,
                algo_params=algo_params,
                render_params=DCN1985RenderParams(
                    super_title="World",
                    title="Exports from Sri Lanka (USD M.)",
                    footer_text="Data Source: United Nations COMTRADE database (2023)",
                    end_value_color='green',
                ),
            )
        ],
    ]
    GridCAC(dcn_list_list).build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )


if __name__ == "__main__":
    main()
