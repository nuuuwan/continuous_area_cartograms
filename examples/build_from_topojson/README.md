# Build From Topojson

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/build_from_topojson/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from cac import DCN1985

    algo = DCN1985.from_topojson(
        topojson_path=os.path.join(
            os.path.dirname(__file__), 'topojson_data', 'DSDivisions.json'
        ),
    )

    algo.build(
        os.path.join(
            os.path.dirname(__file__),
        )
    )

if __name__ == "__main__":
    main()

```
