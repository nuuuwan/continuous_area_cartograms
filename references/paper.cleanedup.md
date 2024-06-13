# An Algorithm to Construct Continuous Area Cartograms  

**Authors:** James A. Dougenik, Nicholas R. Chrisman, Duane R. Niemeyer  
**Locations:** Bedford, MA; University of Wisconsin, Madison; Reading, MA

## Abstract

Continuous area cartograms distort planimetric maps to produce a desired set of areas while preserving the topology of the original map. The authors present a computer algorithm which achieves this result iteratively with high accuracy. The approach uses a model of forces exerted from each polygon centroid, acting on coordinates in inverse proportion to distance. This algorithm can handle more realistic descriptions of polygon boundaries than previous algorithms and manual methods, thus enhancing visual recognition.

**Key Words:** cartograms, thematic cartography, computer cartography, transformations, distortion of maps.

## Introduction

Cartograms are controversial in part because they are difficult to construct and the results seen to date are crude or imprecise, or both. They also may communicate poorly to some audiences. The proposed computer algorithm attempts to redress the balance by providing a new approach to constructing precise cartograms.

### Definition of Cartogram

A cartogram is a map that is purposely distorted so that its spatial properties represent quantities not directly associated with position on the globe. As thematic maps, cartograms emphasize the distribution of a variable by changing the area (or lengths) of objects on the map. There are two broad categories of cartograms:

- **Linear Cartograms**: These express one-dimensional quantities by altering the distance components of maps.
- **Area Cartograms**: These use two-dimensional distortions to represent thematic information.

Since the two forms have distinct methods of construction, our discussion will focus exclusively on area cartograms. Within area cartograms, the largest distinction concerns continuity; they can be produced by sacrificing continuity and surrounding all zones with varying amounts of blank space. Despite this alternative, the traditional form of a cartogram remains the continuous area technique, discussed as long ago as 1934 by Raisz. Considering the long-term interest in continuous area cartograms, an effective computer algorithm to construct them is desired. Our approach maintains continuity and preserves many local features of cartographic lines that provide visual clues to the identity of the distorted objects.

### Chronology of Cartogram Algorithms

The only previous publication presenting an algorithm for continuous area cartograms was by Tobler in 1973. He used a two-step process:

1. **Base Map Fixation**: First, fix the base map to a continuous surface representing the thematic variable.
2. **Projection**: Then, project the map onto a new plane, introducing some distortion. This projection minimizes the Jacobian determinant of the surface as an approximation of the new areas, but the new areas relate to a cellular grid, not the original polygons.

Through successive iterations involving a quadratic function of differences between desired and actual areas, the approximation is improved. The quadratic method provides a new area for each cell, but it does not assure that the projection is a continuous function. Tobler describes the final convergence of the method as slow because a topological test is needed to prevent cell corners from crossing cell boundaries. In his example (a U.S. state cartogram of 1970 population), convergence was far from complete after 99 iterations. The areas achieved only showed a correlation coefficient of .6 with the areas intended, implying an explanation of only 36 percent of the variance. This result shows distortion in the correct direction, but the result is a cartogram of a different variable from the one intended.

The insufficient accuracy of Tobler's results led Chrisman to outline a new approach using rubber sheet distortion. The cartogram process was applied directly to the topological structure of the map, not through an intermediary surface. Each polygon exerted a force on the adjacent boundary nodes, producing a vector result, when summed for all adjacent polygons, that displaced the node's position. The force was proposed to be proportional to the signed square root of the difference between current and desired area. This transformation converts a ratio of areas to a ratio of positions. The force was proposed to act from a polygon center on the nodes of that polygon's boundary. All the forces of polygons adjacent to a node are summed to displace the node to a new location. Like Tobler, Chrisman planned an iterative cycle with new areas and coordinates replacing the previous ones.
