#!/usr/bin/env python
from pxr import Usd, UsdGeom

# Open a stage for writing
stage = Usd.Stage.CreateNew("simple.usda")
shapeMesh = UsdGeom.Sphere.Define(stage, f"/World/Sphere")
# Define a sphere mesh in the world
# get the primitive we have just created and set a translate on it
prim = shapeMesh.GetPrim()
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(10)
frame = 0
for x in range(-10, 10, 2):
    UsdGeom.XformCommonAPI(prim).SetTranslate((x, 0, 0), time=frame)
    frame += 1

# print out the stage and then save it
print(stage.GetRootLayer().ExportToString())
stage.GetRootLayer().Save()
