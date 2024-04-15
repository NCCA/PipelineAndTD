#!/usr/bin/env python
import math
import random

from pxr import Gf, Usd, UsdGeom


# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("curves.usda")

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = "World"
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0)


curve_prim = UsdGeom.BasisCurves.Define(stage, "/World/Curves")
# curve_prim.GetBasisAttr().Set("catmullRom")
points = [Gf.Vec3f(0, 0, 0), Gf.Vec3f(-0.5, 0.5, 0), Gf.Vec3f(0.5, 1, 0)]
# points = [(0, 0, 0), (-1, -0.5, 1), (2, 0.5, 1), (1, 0, -1)]
curve_prim.CreatePointsAttr().Set(points)
vertex_counts = [3]
curve_prim.CreateCurveVertexCountsAttr().Set(vertex_counts)

widths = [0.01, 0.01, 0.01]
curve_prim.CreateWidthsAttr().Set(widths)
# Print out the stage
print(stage.GetRootLayer().ExportToString())
# Save the resulting layer
stage.Export("curves.usda", addSourceFileComment=True)
