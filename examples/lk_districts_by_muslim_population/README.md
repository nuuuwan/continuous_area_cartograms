# Lk Districts By Muslim Population

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_districts_by_muslim_population/output/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985, DCN1985RenderParams

    gig_table_last_election = GIGTable(
        'population-religion', 'regions', '2012'
    )

    ents = [ent for ent in Ent.list_from_type(EntType.DISTRICT)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.islam)

    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            title="Sri Lanka's Districts",
            start_value_unit="km2",
            end_value_unit="Muslim Population",
            start_total_value=65_610,
        ),
    )
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

if __name__ == "__main__":
    main()

```
