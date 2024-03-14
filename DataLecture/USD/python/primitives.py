#!/usr/bin/env python
from pxr import Usd, UsdGeom

def position_prim(prim: Usd.Prim, translate: tuple) -> None:
    UsdGeom.XformCommonAPI(prim).SetTranslate(translate)


# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("Cube.usda")

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = 'World'   
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0) 

shapeMesh = UsdGeom.Sphere.Define(stage, "/World/Sphere")
position_prim(shapeMesh.GetPrim(), (1, 0, 1))
shapeMesh = UsdGeom.Cube.Define(stage, "/World/Cube")
position_prim(shapeMesh.GetPrim(), (-1, 0, 1))

# Add transforms to the cube
# UsdGeom.XformCommonAPI(prim).SetRotate((0, 45.0, 0))
# UsdGeom.XformCommonAPI(prim).SetTranslate((1, 0, 0))
# UsdGeom.XformCommonAPI(prim).SetScale((1, 2.0, 1.0))

# Print out the stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("primitives.usda", addSourceFileComment=True)