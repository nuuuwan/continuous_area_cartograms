import os


def main():  # noqa
    from gig import Ent, EntType

    from cac import (DCN1985, DCN1985AlgoParams, DCN1985RenderParams,
                     MultiStageCAC)

    ents = Ent.list_from_type(EntType.PROVINCE)
    values_population = [ent.population for ent in ents]
    # Source:
    # https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/press/pr/press_pgdp_2022_e.pdf
    PROVINCE_ID_TO_GDP = {
        'LK-1': 10_473_166,
        'LK-2': 2_423_253,
        'LK-3': 2_199_791,
        'LK-4': 985_139,
        'LK-5': 1_248_306,
        'LK-6': 2_706_227,
        'LK-7': 1_209_771,
        'LK-8': 1_176_221,
        'LK-9': 1_725_853,
    }
    values_gdp = [PROVINCE_ID_TO_GDP[ent.id] for ent in ents]
    algo_params = DCN1985AlgoParams(
        max_iterations=20,
    )

    MultiStageCAC(
        DCN1985.from_ents(
            ents,
            values_population,
            algo_params=algo_params,
            render_params=DCN1985RenderParams(
                title="Sri Lanka's Provinces",
                start_value_unit="Area (km2)",
                end_value_unit="Population",
                start_total_value=65_610,
                start_value_hue=240,
                end_value_hue=120,
            ),
        ),
        DCN1985.from_ents(
            ents,
            values_gdp,
            algo_params=algo_params,
            render_params=DCN1985RenderParams(
                title="Sri Lanka's Provinces",
                start_value_unit="Area (km2)",
                end_value_unit="GDP (LKR M)",
                start_total_value=65_610,
                end_value_hue=0,
            ),
        ),
    ).run(
        os.path.join(
            os.path.dirname(__file__),
        )
    )


if __name__ == "__main__":
    main()
