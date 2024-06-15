<<<<<<< HEAD
# Build From Topojson

<p align="center">
    ![https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_topojson/output/animated.gif](https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_topojson/output/animated.gif)
</p>

```python
def main():
    import os

    from cac import DCN1985

    algo = DCN1985.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'DSDivisions.json'
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
=======
### [Build From Topojson](examples/build_from_topojson)

<p align="center">

  <a href="https://github.com/nuuuwan/continuous_area_cartograms/tree/main/examples/build_from_topojson">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_topojson/output/animated.gif" height="240px" />
  </a>

</p>

```python
    import os

    from cac import DCN1985

    algo = DCN1985.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'DSDivisions.json'
        ),
    )

    algo.run(
        os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

```
>>>>>>> 782cfb2a7ef7d410005237e8393216b174716502
