# Continuous Area Cartogram - Examples

## Examples

### [Example 1 From Topojson](examples/example_1_from_topojson)

![Example 1 From Topojson](examples/example_1_from_topojson/output/animated.gif)

```python
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join('example_data', 'Provinces.json'),
        values=[3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    )

    dnc.run(
        dir_output=os.path.join(
            'example_images',
            'example_1_from_topojson',
        )
    )

```

### [Example 2 From Ents](examples/example_2_from_ents)

![Example 2 From Ents](examples/example_2_from_ents/output/animated.gif)

```python
    import os

    from gig import Ent

    from cac import DNC

    ents = Ent.list_from_id_list(['LK-11', 'LK-12', 'LK-13'])
    values = [3, 2, 1]
    dnc = DNC.from_ents(ents, values)
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```

### [Example 3 From Ents By Population](examples/example_3_from_ents_by_population)

![Example 3 From Ents By Population](examples/example_3_from_ents_by_population/output/animated.gif)

```python
    import os

    from gig import Ent, EntType

    from cac import DNC

    ents = Ent.list_from_type(EntType.DISTRICT)
    values = []
    for ent in ents:
        values.append(ent.population)

    dnc = DNC.from_ents(ents, values)
    dir_output = os.path.join(
        'example_images',
        os.path.basename(__file__)[:-3],
    )
    dnc.run(dir_output)

```

### [Example 4 Pds](examples/example_4_pds)

![Example 4 Pds](examples/example_4_pds/output/animated.gif)

```python
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DNC

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = [ent for ent in Ent.list_from_type(EntType.PD)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.electors)

    dnc = DNC.from_ents(ents, values)
    dir_output = os.path.join(
        'example_images',
        os.path.basename(__file__)[:-3],
    )
    dnc.run(dir_output)

```
