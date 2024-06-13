# Examples

### [Build From Ents](examples/build_from_ents)

<p align="center">
  <img src="build_from_ents/output/animated.gif" width="240px" />
</p>

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

### [Build From Polygons](examples/build_from_polygons)

<p align="center">
  <img src="build_from_polygons/output/animated.gif" width="240px" />
</p>

```python
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'Provinces.json'
        ),
        values=[1, 1, 3, 1, 1, 1, 1, 1, 1, 1],  # LK-11 - Western Province
    )

    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```

### [Build From Topojson](examples/build_from_topojson)

<p align="center">
  <img src="build_from_topojson/output/animated.gif" width="240px" />
</p>

```python
    import os

    from cac import DNC

    dnc = DNC.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'Provinces.json'
        ),
        values=[1, 1, 3, 1, 1, 1, 1, 1, 1],  # LK-11 - Western Province
    )

    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```

### [Lk Districts By Population](examples/lk_districts_by_population)

<p align="center">
  <img src="lk_districts_by_population/output/animated.gif" width="240px" />
</p>

```python
    import os

    from gig import Ent, EntType

    from cac import DNC

    ents = Ent.list_from_type(EntType.DISTRICT)
    values = []
    for ent in ents:
        values.append(ent.population)

    dnc = DNC.from_ents(ents, values)
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```

### [Lk Pds By Electors](examples/lk_pds_by_electors)

<p align="center">
  <img src="lk_pds_by_electors/output/animated.gif" width="240px" />
</p>

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
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
