# Continuous Area Cartograms

Implements *[An Algorithm to Construct Continuous Area Cartograms](paper.pdf)* by Dougenik, Chrisman, and Niemeyer (1985).

## Examples

### [Example 1 From Topojson](examples/example_1_from_topojson)

![Example 1 From Topojson](examples/example_1_from_topojson/output/animated.gif)

### [Example 2 From Ents](examples/example_2_from_ents)

![Example 2 From Ents](examples/example_2_from_ents/output/animated.gif)

### [Example 3 From Ents By Population](examples/example_3_from_ents_by_population)

![Example 3 From Ents By Population](examples/example_3_from_ents_by_population/output/animated.gif)

### [Example 4 Pds](examples/example_4_pds)

![Example 4 Pds](examples/example_4_pds/output/animated.gif)

See more [Examples](README.examples.long.md).

## Usage

I plan to deploy this as a PyPI package, but for now you can clone the repository, install the dependencies, and run the code directly. You might also find the following [examples](examples) useful.

### TODOs before deployment

* Implement derivations like HexBin
* Simplify and improve the API, which is still a little disorganized.
* Add options to save polygons, as GDF, TopoJSON etc
* Improve [examples](src/cac/examples). Have single examples folder, with sub-folders for data, source and images.
* Generate some more complex examples.

## Algorithm described in [paper](paper.pdf)

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
