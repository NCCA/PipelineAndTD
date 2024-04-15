#!/usr/bin/env python
from pxr import Usd, UsdGeom

# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("Cube.usda")
# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/Cube")
# Set a translation
UsdGeom.XformCommonAPI(xformPrim).SetTranslate((0, 0, 0))

cubePrim = UsdGeom.Cube.Define(stage, "/Cube/MeshData")

# Get the sphere as a generic prim
cube = stage.GetPrimAtPath("/Cube/MeshData")

# Get the dimensions
size = cubePrim.GetSizeAttr()

# Access the cube schema to set the color
colorAttr = cubePrim.GetDisplayColorAttr()

size.Set(2.9)


# Make the cube blue
colorAttr.Set([(0.0, 0.0, 1.0)])

# Print out the stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("BlueCube.usda", addSourceFileComment=False)
