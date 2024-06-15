# Southern Province Dsds By Population

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/southern_province_dsds_by_population/output/animated.gif" alt="alt" />
</p>

```python
def main():
    import os

    from gig import Ent, EntType

    from cac import DCN1985

    ents = Ent.list_from_type(EntType.DSD)
    ents = [ent for ent in ents if ent.province_id in ['LK-3']]
    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(ents, values, preprocess_tolerance=0.0)
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

if __name__ == "__main__":
    main()

```
