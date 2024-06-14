### [Lk Pds By Electors](examples/lk_pds_by_electors)

<p align="center">

  <a href="examples/lk_pds_by_electors">
    <img src="examples/lk_pds_by_electors/output/animated.gif" height="320px" />
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
