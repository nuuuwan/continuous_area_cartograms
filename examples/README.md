# Examples

### [Build From Ents](examples/build_from_ents)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_ents">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_ents/output/animated.gif" height="240px" />
  </a>

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

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_polygons">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_polygons/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from shapely import Polygon

    from cac import DNC

    polygons = [
        Polygon(
            [
                (0, 0),
                (0, 1),
                (1, 1),
                (1, 0),
                (0, 0),
            ]
        ),
        Polygon(
            [
                (1, 0),
                (1, 1),
                (2, 1),
                (2, 0),
                (1, 0),
            ]
        ),
        Polygon(
            [
                (0, 1),
                (0, 2),
                (1, 2),
                (1, 1),
                (0, 1),
            ]
        ),
        Polygon(
            [
                (1, 1),
                (1, 2),
                (2, 2),
                (2, 1),
                (1, 1),
            ]
        ),
    ]

    dnc = DNC(
        polygons,
        [1, 4, 1, 1],
    )

    new_polygon = dnc.run(
        dir_output=os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

    print(new_polygon)

    # [<POLYGON ((0.032 0.232, 0.142 0.979, 0.68 1.32, 0.587 0.078, 0.032 0.232))>, <POLYGON ((0.587 0.078, 0.68 1.32, 1.922 1.413, 2.122 -0.122, 0.587 0.078))>, <POLYGON ((0.142 0.979, 0.112 1.888, 1.021 1.858, 0.68 1.32, 0.142 0.979))>, <POLYGON ((0.68 1.32, 1.021 1.858, 1.768 1.968, 1.922 1.413, 0.68 1.32))>]

```

### [Build From Topojson](examples/build_from_topojson)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_topojson">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_topojson/output/animated.gif" height="240px" />
  </a>

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

### [Cmb Pds By Population](examples/cmb_pds_by_population)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/cmb_pds_by_population">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/cmb_pds_by_population/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from gig import Ent, EntType

    from cac import DNC

    ents = Ent.list_from_type(EntType.PD)
    ents = [ent for ent in ents if ent.ed_id == 'EC-01']
    values = []
    for ent in ents:
        values.append(ent.population)

    dnc = DNC.from_ents(ents, values, preprocess_tolerance=0.0000001)
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```

### [Cmc Gnds By Population](examples/cmc_gnds_by_population)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/cmc_gnds_by_population">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/cmc_gnds_by_population/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from gig import Ent, EntType

    from cac import DNC

    ents = Ent.list_from_type(EntType.GND)
    ents = [ent for ent in ents if ent.dsd_id in ['LK-1103', 'LK-1127']]
    values = []
    for ent in ents:
        values.append(ent.population)

    dnc = DNC.from_ents(ents, values, preprocess_tolerance=0.0)
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```

### [Europe By Gdp Md Est](examples/europe_by_gdp_md_est)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/europe_by_gdp_md_est">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/europe_by_gdp_md_est/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    import geopandas

    from cac import DNC

    gdf = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf = gdf[gdf['continent'] == 'Europe']
    gdf = gdf[gdf['name'] != 'Russia']

    values = gdf['gdp_md_est'].tolist()
    dnc = DNC.from_gdf(
        gdf,
        values,
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

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/lk_districts_by_population">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_districts_by_population/output/animated.gif" height="240px" />
  </a>

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

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/lk_pds_by_electors">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_pds_by_electors/output/animated.gif" height="240px" />
  </a>

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

### [World Countries By Population](examples/world_countries_by_population)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/world_countries_by_population">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/world_countries_by_population/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    import geopandas

    from cac import DNC

    gdf_world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )
    gdf_world = gdf_world[gdf_world['continent'] != 'Antarctica']

    values = gdf_world['pop_est'].tolist()
    dnc = DNC.from_gdf(
        gdf_world,
        values,
        min_log2_error=0.1,
        max_iterations=100,
    )
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
