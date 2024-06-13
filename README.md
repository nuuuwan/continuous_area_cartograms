# Continuous Area Cartograms

<img src="examples/example_3_from_ents_by_population/output/animated.gif" width="240px" />

> An animation of a True-Scale Map of Sri Lanka's Administrative districts, morphing into a Continous Area Cartograms representing population

## Background

### What is a Cartogram?

A cartogram is a map in which some thematic mapping variable, such as population or Gross Domestic Product (GDP), is substituted for land area or distance. The geometry or space of the map is distorted in order to convey the information of this alternate variable. Cartograms help to visualize the relative sizes of the variables in a way that a traditional map does not, making them useful tools in geographical statistics.

### What is a Continuous Area Cartogram (CAC)?

A Continuous Area Cartogram (CAC) is a type of cartogram where the map is distorted gradually and smoothly to reflect a specific variable while maintaining the contiguous nature of regions. Unlike other cartograms that might use non-contiguous shapes or overlapping regions, CACs ensure that all areas are mapped to contiguous regions, preserving neighboring relationships. This makes them more recognizable and easier to understand in terms of geographical layout.

### Why are Cartograms Useful?

Cartograms are especially useful for providing a visual representation of statistical data, allowing for easy comparisons and understanding of geographic distributions of data. They highlight disparities and patterns that might be overlooked in standard map representations. For example, a cartogram can make it visually apparent how much larger the population of one city is compared to another, despite the actual geographic size being smaller.

## This Repository

This repository Implements *[An Algorithm to Construct Continuous Area Cartograms](references/paper.pdf)* by Dougenik, Chrisman, and Niemeyer (1985).

## Example images and code

See [Examples](README.examples.md).

## Usage

We plan to deploy this as a PyPI package soon.

For now you may clone/fork the repository, install the dependencies, and run the code directly.

### TODOs before PyPI deployment

* Simplify and improve the API, which is still a little disorganized.
* Generate some more complex examples.

## Algorithm described in [paper](references/paper.pdf)

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
