# Lk Pds In Units

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_pds_in_units/output/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985RenderParams

    ents = Ent.list_from_type(EntType.PD)
    values = [1 for _ in ents]
    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            title="Sri Lanka's Polling Divisions",
            start_value_unit="km2",
            end_value_unit="Units",
            start_total_value=65_610,
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
