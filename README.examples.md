# Examples

## [example_1_from_topojson.py](examples/example_1_from_topojson.py)

![examples\example_1_from_topojson.py](example_images\example_1_from_topojson\animated.gif)

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

![examples\example_2_from_ents.py](example_images\example_2_from_ents\animated.gif)

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

## [example_3_pds.py](examples/example_3_pds.py)

![examples\example_3_pds.py](example_images\example_3_pds\animated.gif)

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
    dir_output = os.path.join(
        'example_images',
        os.basename(__file__)[:-3],
    )
    dnc.run(
        dir_output=dir_output
    )

```
