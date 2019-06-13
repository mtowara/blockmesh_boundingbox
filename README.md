Creates from a given stl a bounding box for OpenFOAMs blockMesh utility. Useful for snappyHexMesh / cfMesh meshing.
The created bounding box can either be aligned to xyz coordinate sytem or along custom orthogonal axes.

Output is put to stdout and should be redirected to a blockMeshDict file.
Spacing adjusts the number of cells to create in each direction, extra-margin add extra padding around the geometry.

Usage examples:
```
./createBoundingBox.py --extra-margin 0.05 --spacing 2.0 test.stl
./createBoundingBoxCustomAxes.py --extra-margin 0.05 --spacing 2.0 -d1 49.497 35.000 -35.00 -d2 0.000 7.071 7.071 test.stl 
```

Example blockMesh:

<img src=".doc/demo.png" alt="test.stl" width="500"/>
