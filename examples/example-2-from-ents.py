import os
from utils import Log
from gig import Ent, EntType
from cac import DNC

def from_ents(ent_type):
    ents = [ent for ent in Ent.list_from_type(ent_type)]
    id_to_value = {}
    total_population = sum(ent.population for ent in ents)
    for ent in ents:
        population = ent.population
        value = population / total_population
        id_to_value[ent.id] = value

    dnc = DNC.from_ents(ents, id_to_value)
    dnc.run(file_label=f"ents.{ent_type.name}", n=10)


if __name__ == "__main__":
    from_ents(EntType.DISTRICT) 
    from_ents(EntType.PROVINCE)
    