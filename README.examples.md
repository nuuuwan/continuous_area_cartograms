# Examples

## [example_1_from_topojson.py](examples/example_1_from_topojson.py)

```python
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join('example_data', 'Provinces.json'),
        get_ids=lambda gdf: gdf['prov_c'],
    )

    dnc.run(
        dir_output=os.path.join(
            'example_images',
            'example_1_from_topojson',
        )
    )

```

## [example_2_from_ents.py](examples/example_2_from_ents.py)

```python
    import os

    from gig import Ent

    from cac import DNC

    id_to_value = {
        'LK-11': 3,
        'LK-12': 2,
        'LK-13': 1,
    }
    ents = Ent.list_from_id_list(id_to_value.keys())

    dnc = DNC.from_ents(ents, id_to_value)
    dnc.run(
        dir_output=os.path.join(
            'example_images',
            'example_2_from_ents',
        )
    )

```

## [example_3_from_ents_complex.py](examples/example_3_from_ents_complex.py)

```python

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

```

## [example_4_pds.py](examples/example_4_pds.py)

```python
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DNC

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = [ent for ent in Ent.list_from_type(EntType.PD)]
    id_to_value_num = {}
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        electors = row.electors
        id_to_value_num[ent.id] = electors

    total_electors = sum(id_to_value_num.values())
    id_to_value = {
        id: electors / total_electors
        for id, electors in id_to_value_num.items()
    }

    dnc = DNC.from_ents(ents, id_to_value)
    dnc.run(
        dir_output=os.path.join(
            'example_images',
            os.basename(__file__)[:-3],
        )
    )

```
