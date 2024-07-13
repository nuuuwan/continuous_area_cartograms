# Lk Provinces By Gdp

<p  align="center">
    <img src="https://raw.githubusercontent.com/nuuuwan/continuous_area_cartograms/main/examples/examples/lk_provinces_by_gdp/animated.gif" alt="alt" />
</p>

```python
def main():  # noqa
    import os

    from gig import Ent, EntType

    from cac import DCN1985, DCN1985RenderParams, HexBin

    ents = Ent.list_from_type(EntType.PROVINCE)

    # Source:
    # https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/press/pr/press_pgdp_2022_e.pdf
    GDP_DATA_IDX = {
        'LK-1': 10_473_166,
        'LK-2': 2_423_253,
        'LK-3': 2_199_791,
        'LK-4': 985_139,
        'LK-5': 1_248_306,
        'LK-6': 2_706_227,
        'LK-7': 1_209_771,
        'LK-8': 1_176_221,
        'LK-9': 1_725_853,
    }

    values = []
    for ent in ents:
        values.append(GDP_DATA_IDX[ent.id])

    algo = DCN1985.from_ents(
        ents,
        values,
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Provinces",
            title="GDP (LKR M)",
        ),
    )
    polygons = algo.run(
        os.path.join(
            os.path.dirname(__file__),
        ),
    )

    HexBin(polygons).save_hexbin(
        os.path.join(
            os.path.dirname(__file__),
            'hexbin.png',
        )
    )

if __name__ == "__main__":
    main()

```
