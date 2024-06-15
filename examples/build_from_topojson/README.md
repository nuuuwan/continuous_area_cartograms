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
