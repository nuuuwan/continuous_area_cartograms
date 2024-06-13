# Continuous Area Cartograms

<p align="center">
  <img src="examples/build_from_polygons/output/animated.gif" width="240px" />

  <img src="examples/cmc_gnds_by_population/output/animated.gif" width="240px" />

  <img src="examples/cmb_pds_by_population/output/animated.gif" width="240px" />

  <img src="examples/build_from_ents/output/animated.gif" width="240px" />

  <img src="examples/build_from_topojson/output/animated.gif" width="240px" />

  <img src="examples/lk_districts_by_population/output/animated.gif" width="240px" />

  <img src="examples/lk_pds_by_electors/output/animated.gif" width="240px" />
</p>

> An animation of a True-Scale Map of Sri Lanka's Administrative districts, morphing into a Continous Area Cartograms representing population

## Background

### What is a Cartogram?

A cartogram is a map in which some thematic mapping variable, such as population or Gross Domestic Product (GDP), is substituted for land area or distance. The geometry or space of the map is distorted in order to convey the information of this alternate variable. Cartograms help to visualize the relative sizes of the variables in a way that a traditional map does not, making them useful tools in geographical statistics.

### What is a Continuous Area Cartogram (CAC)?

A Continuous Area Cartogram (CAC) is a type of cartogram where the map is distorted gradually and smoothly to reflect a specific variable while maintaining the contiguous nature of regions. Unlike other cartograms that might use non-contiguous shapes or overlapping regions, CACs ensure that all areas are mapped to contiguous regions, preserving neighboring relationships. This makes them more recognizable and easier to understand in terms of geographical layout.

### Why are Cartograms Useful?

Cartograms are especially useful for providing a visual representation of statistical data, allowing for easy comparisons and understanding of geographic distributions of data. They highlight disparities and patterns that might be overlooked in standard map representations. For example, a cartogram can make it visually apparent how much larger the population of one city is compared to another, despite the actual geographic size being smaller.

## This Repository

This repository implements Dougenik, Chrisman, and Niemeyer's algorithm, which they described in the 1985 paper, *[An Algorithm to Construct Continuous Area Cartograms](references/paper.pdf)*.

## Install

```bash
pip install continuous_area_cartograms-nuuuwan
```

## Examples

<p align="center">
  <img src="examples/build_from_polygons/output/animated.gif" width="240px" />
</p>

First, construct a **DNC object**, providing the regions (as shapely Polygons) and their corresponding values.

Second, call **run** which returns a new polygon, appropriately modified.

```python
    import os

    from shapely import Polygon

    from cac import DNC

    polygons = [
        Polygon(
            [
                (0, 0),
                (0, 1),
                (1, 1),
                (1, 0),
                (0, 0),
            ]
        ),
        Polygon(
            [
                (1, 0),
                (1, 1),
                (2, 1),
                (2, 0),
                (1, 0),
            ]
        ),
        Polygon(
            [
                (0, 1),
                (0, 2),
                (1, 2),
                (1, 1),
                (0, 1),
            ]
        ),
        Polygon(
            [
                (1, 1),
                (1, 2),
                (2, 2),
                (2, 1),
                (1, 1),
            ]
        ),
    ]

    dnc = DNC(
        polygons,
        [1, 4, 1, 1],
    )

    new_polygon = dnc.run(
        dir_output=os.path.join(
            os.path.dirname(__file__),
            'output',
        )
    )

    print(new_polygon)

```

Output:

```bash
[<POLYGON ((0.032 0.232, 0.142 0.979, 0.68 1.32, 0.587 0.078, 0.032 0.232))>, <POLYGON ((0.587 0.078, 0.68 1.32, 1.922 1.413, 2.122 -0.122, 0.587 0.078))>, <POLYGON ((0.142 0.979, 0.112 1.888, 1.021 1.858, 0.68 1.32, 0.142 0.979))>, <POLYGON ((0.68 1.32, 1.021 1.858, 1.768 1.968, 1.922 1.413, 0.68 1.32))>]
```

The output directory stores the following content:

* geojson: GeoJSON files for each step of the algorithm
* images: Rendered images for each step of the algorithm
* animated.gif: Images combined into an animated GIF

Alternatively, DNCs objects can be constructed from [geopandas.GeoDataFrame](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.html) objects, [TopoJSON](https://openlayers.org/en/latest/examples/topojson.html), [GeoJSON](https://geojson.org/) or [gig.Ent](https://github.com/nuuuwan/gig) objects.

```python
    @classmethod
    def from_gdf(cls, gdf: gpd.GeoDataFrame, values: list[float], **kwargs):
        ...

    @classmethod
    def from_geojson(cls, geojson_path: str, values: list[float], **kwargs):
        ...

    @classmethod
    def from_topojson(cls, topojson_path: str, values: list[float], **kwargs):
        ...

    @classmethod
    def from_ents(cls, ents: list[Ent], values: list[float], **kwargs):
        ...
```

For more details and source code, see [examples/README.md](examples/README.md).

### TODOs before PyPI deployment

* Simplify and improve the API, which is still a little disorganized.
* Generate some more complex examples.

## The [Algorithm](references/paper.pdf)

```pseudocode
For each polygon
    Read and store PolygonValue (negative value illegal)
    Sum PolygonValue into TotalValue
 
For each iteration (user controls when done)
    For each polygon
        Calculate area and centroid (using current boundaries)
    Sum areas into TotalArea
    
    For each polygon
        Desired = (TotalArea * (PolygonValue / TotalValue))
        Radius = √ (Area / 𝜋)
        Mass = √ (Desired / 𝜋) - √ (Area / 𝜋)
        SizeError = Max(Area, Desired) / Min(Area, Desired)
    ForceReductionFactor = 1 / (1 + Mean (SizeError))

    For each boundary line; Read coordinate chain
        For each coordinate pair
            For each polygon centroid
                Find angle, Distance from centroid to coordinate
                    If (Distance > Radius of polygon)
                        Fij = Mas * (Radius / Distance)
                    Else
                        Fij = Mass * (Distance² / Radius²) * (4 - 3 * (Distance / Radius))
            Using Fij and angles, calculate vector sum
            Multiply by ForceReductionFactor
            Move coordinate accordingly
        Write distorted line to output and plot result
```

In code, we will refer to this as the *DNC Algorithm*, after its authors.

### Intuition

The intuition behind DNC, is as follows:

Our map is a collection of polygons, each representing a region. Some polygons need to be expanded, while others need to be contracted.

Every polygon influences how every point in every polygon is moved to achieve the expansion/contraction. Hence, the algorithm is *O(nm)*, where *n = number of polygons* and *m = number of points in each polygon*.
