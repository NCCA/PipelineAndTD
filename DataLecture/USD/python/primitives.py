#!/usr/bin/env -S uv run --script
from pxr import Usd, UsdGeom


def position_prim(prim: Usd.Prim, translate: tuple) -> None:
    UsdGeom.XformCommonAPI(prim).SetTranslate(translate)


# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("Cube.usda")

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = "World"
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0)

shapeMesh = UsdGeom.Sphere.Define(stage, "/World/Sphere")
position_prim(shapeMesh.GetPrim(), (2, 0, 0))
shapeMesh = UsdGeom.Cube.Define(stage, "/World/Cube")
position_prim(shapeMesh.GetPrim(), (-2, 0, 2))

shapeMesh = UsdGeom.Cone.Define(stage, "/World/Cone")
position_prim(shapeMesh.GetPrim(), (2, 0, 2))

shapeMesh = UsdGeom.Capsule.Define(stage, "/World/Capsule")
position_prim(shapeMesh.GetPrim(), (2, 0, -2))

shapeMesh = UsdGeom.Cylinder.Define(stage, "/World/Cylinder")
position_prim(shapeMesh.GetPrim(), (-2, 0, -2))


# a row of cylinders with different axis
shapeMesh = UsdGeom.Cylinder.Define(stage, "/World/CylinderXAxis")
position_prim(shapeMesh.GetPrim(), (-2, 0, -4))
prim = shapeMesh.GetPrim()
shapeMesh.CreateAxisAttr("X")


shapeMesh = UsdGeom.Cylinder.Define(stage, "/World/CylinderYAxis")
position_prim(shapeMesh.GetPrim(), (0, 0, -4))
prim = shapeMesh.GetPrim()
shapeMesh.CreateAxisAttr("Y")

shapeMesh = UsdGeom.Cylinder.Define(stage, "/World/CylinderZAxis")
position_prim(shapeMesh.GetPrim(), (2, 0, -4))
prim = shapeMesh.GetPrim()
shapeMesh.CreateAxisAttr("Z")


# Print out the stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("primitives.usda", addSourceFileComment=True)
