# Continuous Area Cartograms

Implements *[An Algorithm to Construct Continuous Area Cartograms](paper.pdf)* by Dougenik, Chrisman, and Niemeyer (1985).

## Examples

### Provinces of Sri Lanka :sri_lanka:

![example-2](images/ents.province/animated.gif)

### Districts of Sri Lanka :sri_lanka:

![example-2](images/ents.district/animated.gif)

### Polling Divisions in the Western Province, Sri Lanka

![example-2](images/ents.pd.western/animated.gif)

### Polling Divisions in Colombo, Sri Lanka

![example-2](images/ents.pd.colombo/animated.gif)

## Procedure described in paper

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
                        Fij = Mass * (Distance ^ 2 / Radius ^ 2) * (4 - 3 * (Distance / Radius))
            Using Fij and angles, calculate vector sum
            Multiply by ForceReductionFactor
            Move coordinate accordingly
        Write distorted line to output and plot result
```

In code, we will refer to this as the *DNC Algorithm*, after its authors.
