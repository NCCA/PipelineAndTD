#!/usr/bin/env python
from pxr import Usd, UsdGeom

# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("Cube.usda")

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")


prim = UsdGeom.Mesh.Define(stage, "/World/Cube")
prim.CreatePointsAttr().Set([(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5)])
prim.CreateFaceVertexCountsAttr().Set([4, 4, 4, 4, 4, 4])
prim.CreateFaceVertexIndicesAttr().Set([0, 1, 3, 2, 2, 3, 5, 4, 4, 5, 7, 6, 6, 7, 1, 0, 1, 7, 5, 3, 6, 0, 2, 4])
prim.CreateExtentAttr().Set([(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)])

# Set the color of the cube
colorAttr = prim.GetDisplayColorAttr()
colorAttr.Set([(0.463, 0.725, 0.0)])

# Add transforms to the cube
UsdGeom.XformCommonAPI(prim).SetRotate((0, 45.0, 0))
UsdGeom.XformCommonAPI(prim).SetTranslate((1, 0, 0))
UsdGeom.XformCommonAPI(prim).SetScale((1, 2.0, 1.0))


# Print out the stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("cube.usda", addSourceFileComment=False)