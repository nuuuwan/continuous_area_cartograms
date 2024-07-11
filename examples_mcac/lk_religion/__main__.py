import os


def main():  # noqa
    from gig import Ent, EntType, GIGTable

    from cac import (DCN1985, DCN1985AlgoParams, DCN1985RenderParams,
                     MultiStageCAC)

    ent_type = EntType.PROVINCE
    ents = Ent.list_from_type(ent_type)
    values_population = [ent.population for ent in ents]
    algo_params = DCN1985AlgoParams(
        max_iterations=20,

    )

    dnc_list = [
        DCN1985.from_ents(
            ents,
            values_population,
            algo_params=algo_params,
            render_params=DCN1985RenderParams(
                title="Sri Lanka's " + ent_type.name.title() + 's',
                start_value_unit="",
                end_value_unit="Population",
                start_value_hue=330,
                end_value_hue=360,
            ),
        )
    ]

    # religion
    gig_table = GIGTable('population-religion', 'regions', '2012')
    first_row = ents[0].gig(gig_table)
    fields = first_row.dict.keys()
    for field in fields:
        hue = {
            'buddhist': 90,
            'hindu': 60,
            'muslim': 120,
            'christian': 240,
        }.get(field, 300)

        values = []
        for ent in ents:
            row = ent.gig(gig_table)
            values.append(row.dict[field])
        dnc = DCN1985.from_ents(
            ents,
            values,
            algo_params=algo_params,
            render_params=DCN1985RenderParams(
                title="Sri Lanka's " + ent_type.name.title() + 's',
                end_value_unit=field.title(),
                end_value_hue=hue,
            ),
        )
        dnc_list.append(dnc)

    MultiStageCAC(*dnc_list).run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )


if __name__ == "__main__":
    main()
