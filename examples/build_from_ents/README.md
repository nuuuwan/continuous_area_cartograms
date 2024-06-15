<<<<<<< HEAD
# Build From Ents

<p align="center">
    ![https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_ents/output/animated.gif](https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_ents/output/animated.gif)
</p>

```python
def main():
    import os

    from gig import Ent

    from cac import DCN1985

    ents = Ent.list_from_id_list(['LK-11', 'LK-12', 'LK-13'])
    values = [3, 2, 1]
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
### [Build From Ents](examples/build_from_ents)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_ents">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_ents/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from gig import Ent

    from cac import DCN1985

    ents = Ent.list_from_id_list(['LK-11', 'LK-12', 'LK-13'])
    values = [3, 2, 1]
    algo = DCN1985.from_ents(ents, values)
    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
>>>>>>> 782cfb2a7ef7d410005237e8393216b174716502
