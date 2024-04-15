#!/usr/bin/env python
import math
import random

from pxr import Gf, Usd, UsdGeom


def create_blade(pos):
    number_of_points = random.randint(3, 10)
    height = 1.0 + random.uniform(0.1, 2)
    step = height / number_of_points
    points = []
    for i in range(number_of_points):
        points.append(
            Gf.Vec3f(
                pos[0] + random.uniform(-0.1, 0.1),
                pos[1] + i * step,
                pos[2] + random.uniform(-0.1, 0.1),
            )
        )
    return number_of_points, points


# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("grass.usda")

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = "World"
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0)


curve_prim = UsdGeom.BasisCurves.Define(stage, "/World/Curves")
# curve_prim.GetBasisAttr().Set("catmullRom")
points = []
vertex_counts = []

x = -10.0
z = -10.0
while x < 10.0:
    while z < 10.0:
        num, blades = create_blade((x, 0, z))
        points.extend(blades)
        vertex_counts.append(num)
        z += 0.2
    x += 0.2
    z = -10.0


curve_prim.CreatePointsAttr().Set(points)
curve_prim.CreateCurveVertexCountsAttr().Set(vertex_counts)

widths = [0.01]
curve_prim.CreateWidthsAttr().Set(widths)
# Save the resulting layer
stage.Export("grass.usda", addSourceFileComment=True)
