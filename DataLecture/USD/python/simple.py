#!/usr/bin/env python
from pxr import Usd, UsdGeom


# Open a stage for writing
stage = Usd.Stage.CreateNew("simple.usda")
# We need a unique name for the sphere
sphereNumber = 0
# now loop for x and z in steps of 2 (as each sphere has a radius of 2 units )
for x in range(-10, 10, 2):
    for z in range(-10, 10, 2):
        # start numbering the spheres from 1
        sphereNumber += 1
        # Define a sphere mesh in the world
        shapeMesh = UsdGeom.Sphere.Define(stage, f"/World/Sphere{sphereNumber}")
        # get the primitive we have just created and set a translate on it
        prim = shapeMesh.GetPrim()
        UsdGeom.XformCommonAPI(prim).SetTranslate((x, 0, z))

# print out the stage and then save it
print(stage.GetRootLayer().ExportToString())
stage.GetRootLayer().Save()
