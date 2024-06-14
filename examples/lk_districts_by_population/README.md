### [Lk Districts By Population](examples/lk_districts_by_population)

<p align="center">

  <a href="examples/lk_districts_by_population">
    <img src="examples/lk_districts_by_population/output/animated.gif" height="320px" />
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
