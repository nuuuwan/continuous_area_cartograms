### [Cmb Pds By Population](examples/cmb_pds_by_population)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/cmb_pds_by_population">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/cmb_pds_by_population/output/animated.gif" height="320px" />
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

    dnc = DNC.from_ents(ents, values)
    dnc.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
