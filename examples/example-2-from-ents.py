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
    DNC.run(dnc, file_label=f"ents.{label}")


def from_ent_type(ent_type):
    ents = [ent for ent in Ent.list_from_type(ent_type)]
    return from_ents(ents, ent_type.name)


def custom_colombo():
    ents = [
        ent for ent in Ent.list_from_type(EntType.PD) if 'EC-01' in ent.id
    ]
    return from_ents(ents, 'pd.colombo')


def custom_western():
    ents = [
        ent
        for ent in Ent.list_from_type(EntType.PD)
        if ent.id[3:5] in ['01', '02', '03']
    ]
    return from_ents(ents, 'pd.western')


if __name__ == "__main__":
    # from_ent_type(EntType.PROVINCE)
    # from_ent_type(EntType.DISTRICT)
    # from_ent_type(EntType.PD)
    # custom_western()
    custom_colombo()
