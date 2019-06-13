#! /bin/bash

# create othogonal bounding box 
cp -r testCaseStub testCaseOrth
touch testCaseOrth/foam.foam
./createBoundingBox.py --extra-margin 0.05 --spacing 2.0 test.stl > testCaseOrth/system/blockMeshDict
blockMesh -case testCaseOrth

# create bounding box aligned to object
cp -r testCaseStub testCaseCustomAxes
touch testCaseCustomAxes/foam.foam
./createBoundingBoxCustomAxes.py --extra-margin 0.05 --spacing 2.0 -d1 49.497 35.000 -35.00 -d2 0.000 7.071 7.071 test.stl > testCaseCustomAxes/system/blockMeshDict
blockMesh -case testCaseCustomAxes
