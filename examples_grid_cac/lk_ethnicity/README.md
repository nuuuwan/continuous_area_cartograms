# Lk Ethnicity

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples_grid_cac/lk_ethnicity/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import EntType, GIGTable

    from cac import DCN1985RenderParams, GIGTableMCAC

    GIGTableMCAC(
        GIGTable('population-ethnicity', 'regions', '2012'),
        EntType.DISTRICT,
        render_params=DCN1985RenderParams(
            footer_text="Source: " + '2012 Census'
        ),
    ).build(
        os.path.join(
            os.path.dirname(__file__),
        ),
    )

if __name__ == "__main__":
    main()

```
