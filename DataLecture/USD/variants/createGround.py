#!/usr/bin/env -S uv run --script

from pxr import Sdf, Usd, UsdGeom

stage: Usd.Stage = Usd.Stage.CreateInMemory()
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 1.0)

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")


prim = UsdGeom.Mesh.Define(stage, "/World/Cube")
prim.CreatePointsAttr().Set([(-1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1)])
prim.CreateFaceVertexCountsAttr().Set([4])
prim.CreateFaceVertexIndicesAttr().Set([0, 1, 2, 3])
prim.CreateExtentAttr().Set([(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)])
prim.CreateNormalsAttr().Set([(0, 0, 1)])

# Set the color of the cube
colorAttr = prim.GetDisplayColorAttr()
colorAttr.Set([(0.463, 0.725, 0.0)])

# # Add transforms to the cube
# UsdGeom.XformCommonAPI(prim).SetRotate((0, 45.0, 0))
# UsdGeom.XformCommonAPI(prim).SetTranslate((1, 0, 0))
# UsdGeom.XformCommonAPI(prim).SetScale((1, 2.0, 1.0))


usda = stage.GetRootLayer().ExportToString()
print(usda)

stage.Export("ground.usda", addSourceFileComment=False)
