# Build From Ents

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_ents/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent

    from cac import DCN1985

    ents = Ent.list_from_id_list(['LK-11', 'LK-12', 'LK-13'])
    values = [3, 2, 1]
    algo = DCN1985.from_ents(ents, values)
    algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

if __name__ == "__main__":
    main()

```
