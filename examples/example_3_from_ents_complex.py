import os

from gig import Ent, EntType

from cac import DNC


def from_ents(ents, label):
    id_to_value = {}
    total_population = sum(ent.population for ent in ents)
    for ent in ents:
        population = ent.population
        value = population / total_population
        id_to_value[ent.id] = value

    dnc = DNC.from_ents(ents, id_to_value)
    dnc.run(
        dir_output=os.path.join(
            'example_images',
            os.basename(__file__)[:-3] + '.' + label,
        )
    )


def from_ent_type(ent_type):
    ents = [ent for ent in Ent.list_from_type(ent_type)]
    return from_ents(ents, ent_type.name + 's')


def custom_colombo():
    ents = [
        ent for ent in Ent.list_from_type(EntType.PD) if 'EC-01' in ent.id
    ]
    return from_ents(ents, 'pds.colombo')


def custom_western():
    ents = [
        ent
        for ent in Ent.list_from_type(EntType.PD)
        if ent.id in ['EC-01', 'EC-02', 'EC-03']
    ]
    return from_ents(ents, 'pds.western')


def main():
    for ent_type in [EntType.PROVINCE, EntType.DISTRICT, EntType.PD]:
        from_ent_type(ent_type)
    custom_western()
    custom_colombo()


if __name__ == "__main__":
    main()
