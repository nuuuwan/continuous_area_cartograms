<<<<<<< HEAD
# Lk Province By Religion

<p align="center">
    ![https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_province_by_religion/output/animated.gif](https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_province_by_religion/output/animated.gif)
</p>

```python
def main():
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985

    gig_table_last_election = GIGTable(
        'population-religion', 'regions', '2012'
    )

    ents = [ent for ent in Ent.list_from_type(EntType.PROVINCE)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.islam)

    algo = DCN1985.from_ents(ents, values)
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

if __name__ == "__main__":
    main()

```
=======
### [Lk Province By Religion](examples/lk_province_by_religion)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/lk_province_by_religion">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/lk_province_by_religion/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from gig import Ent, EntType, GIGTable

    from cac import DCN1985

    gig_table_last_election = GIGTable(
        'population-religion', 'regions', '2012'
    )

    ents = [ent for ent in Ent.list_from_type(EntType.PROVINCE)]
    values = []
    for ent in ents:
        row = ent.gig(gig_table_last_election)
        values.append(row.islam)

    algo = DCN1985.from_ents(ents, values)
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
>>>>>>> 782cfb2a7ef7d410005237e8393216b174716502
