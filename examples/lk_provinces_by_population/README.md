# Lk Provinces By Population

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_provinces_by_population/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985RenderParams, HexBin

    ents = Ent.list_from_type(EntType.PROVINCE)

    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Provinces",
            title="Population",
        ),
    )
    polygons = algo.run(
        os.path.join(
            os.path.dirname(__file__),
        ),
    )

    HexBin(polygons).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            'hexbin.png',
        )
    )

if __name__ == "__main__":
    main()

```
