# Cmb Pds By Population

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/cmb_pds_by_population/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985AlgoParams, DCN1985RenderParams

    ents = Ent.list_from_type(EntType.PD)
    ents = [ent for ent in ents if ent.ed_id == 'EC-01']
    values = []
    for ent in ents:
        values.append(ent.population)

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            preprocess_tolerance=0.0000001,
        ),
        render_params=DCN1985RenderParams(
            title="Colombo District's Polling Divisions",
            end_value_unit="Population",
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

if __name__ == "__main__":
    main()

```
