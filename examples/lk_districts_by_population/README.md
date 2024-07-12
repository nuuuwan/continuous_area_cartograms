# Lk Districts By Population

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_districts_by_population/output/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams, HexBin

    ents = Ent.list_from_type(EntType.DISTRICT)

    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(max_iterations=10),
        render_params=DCN1985RenderParams(
            title="Sri Lanka's Districts",
            start_value_unit="km2",
            end_value_unit="Population",
            start_total_value=65_610,
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
