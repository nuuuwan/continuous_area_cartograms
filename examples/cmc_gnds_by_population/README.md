### [Cmc Gnds By Population](examples/cmc_gnds_by_population)

<p align="center">

  <a href="cmc_gnds_by_population">
    <img src="cmc_gnds_by_population/output/animated.gif" height="320px" />
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
