# Continuous Area Cartograms

Implements *[An Algorithm to Construct Continuous Area Cartograms](paper.pdf)* by Dougenik, Chrisman, and Niemeyer (1985).

## Usage

I plan to deploy this as a PyPI package, but for now you can clone the repository, install the dependencies, and run the code directly. You might also find the following [examples](examples) useful.

### TODOs before deployment

* Speed-up DAC algorithm, which is still too slow for maps with >20 polygons.
* Simplify and improve the API, which is still a little disorganized
* Improve [examples](src/cac/examples)
* Generate some more complex examples, and possibly run them on a bigger processor on the cloud

## Examples

### Provinces of Sri Lanka

![example-2](images/ents.province/animated.gif)

### Districts of Sri Lanka

![example-2](images/ents.district/animated.gif)

### Polling Divisions in the Western Province, Sri Lanka

![example-2](images/ents.pd.western/animated.gif)

### Polling Divisions in Colombo, Sri Lanka

![example-2](images/ents.pd.colombo/animated.gif)

More example [images](images).

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
