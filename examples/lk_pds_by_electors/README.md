# Lk Pds By Electors

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_pds_by_electors/output/animated.gif" alt="alt" />
</p>

```python
def main():
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985

    gig_table_last_election = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )
    ents = Ent.list_from_type(EntType.PD)

    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.electors)

    algo = DCN1985.from_ents(ents, values, do_shrink=True)
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

if __name__ == "__main__":
    main()

```
