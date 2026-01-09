#!/usr/bin/env -S uv run --script
import math
import random

from pxr import Gf, Usd, UsdGeom


def random_point_on_sphere(radius=1, hemisphere=False):
    xiTheta = random.uniform(0, 1)
    temp = 2.0 * radius * math.sqrt(xiTheta * (1.0 - xiTheta))
    twoPiXiPhi = math.pi * 2 * random.uniform(0, 1)
    x = temp * math.cos(twoPiXiPhi)
    y = temp * math.sin(twoPiXiPhi)
    if hemisphere is True:
        y = abs(y)
    z = radius * (1.0 - 2.0 * xiTheta)
    return Gf.Vec3f(x, y, z)


def random_point(extents: int = 10) -> Gf.Vec3f:
    return Gf.Vec3f(
        random.uniform(-extents, extents),
        random.uniform(-extents, extents),
        random.uniform(-extents, extents),
    )


num_frames = 250
# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("points.usda")
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(num_frames)

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = "World"
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0)

pointsPrim = UsdGeom.Points.Define(stage, "/World/PointSet1")
num_particles = 10000

points = [random_point_on_sphere(10) for _ in range(num_particles)]
pointsPrim.CreatePointsAttr().Set(points, time=0)
# create primvar colours for each point
colors = [Gf.Vec3f(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)) for _ in range(num_particles)]
# pointsPrim.CreateDisplayColorPrimvar(pointsPrim,colors,interpolation=UsdGeom.Tokens.vertex)
pointsPrim.CreateDisplayColorPrimvar("varying").Set(colors)

# colourAttr = pointsPrim.GetDisplayColorAttr()
# colourAttr.setVariability(UsdGeom.Tokens.varying)
# set interpolation to vertex

pointsPrim.CreateWidthsAttr().Set([random.uniform(0.05, 0.1)] * num_particles)
# negate so we can point to the 0,0,0 origin
directions = [-p for p in points]

# now run the Normalize function on each point not you can use list expression to do this
# as the normalize function also returns a float value
for i in range(len(directions)):
    directions[i].Normalize()

directions = [p * random.uniform(0.01, 0.1) for p in directions]
# now calculate p*dir for each of the points and directions
new_points = [p + d for p, d in zip(points, directions, strict=False)]

for frame in range(1, num_frames):
    pointsPrim.CreatePointsAttr().Set(new_points, time=frame)
    new_points = [p + d for p, d in zip(new_points, directions, strict=False)]


# Print out the stage
# print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("points.usdc", addSourceFileComment=True)
