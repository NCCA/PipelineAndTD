#!/usr/bin/env python
import math
import random

from pxr import Gf, Usd, UsdGeom, Sdf


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


def random_scale(min: float = 0.4, max: float = 1.2) -> Gf.Vec3f:
    return Gf.Vec3f(
        random.uniform(min, max),
        random.uniform(min, max),
        random.uniform(min, max),
    )


num_frames = 250
# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("points.usda")
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(num_frames)

UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = "World"
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0)

cube = UsdGeom.Cube(stage.DefinePrim("/World/Cube", "Cube"))
cube.AddScaleOp().Set(Gf.Vec3d(0.1, 0.1, 0.1))
# cube.CreateDisplayColorPrimvar().Set([(0, 1, 1)])

# create our point instancer
instancer = UsdGeom.PointInstancer.Define(stage, "/World/PointInstancer")

num_particles = 200

points = [random_point_on_sphere(10) for _ in range(num_particles)]
positions_attr = instancer.CreatePositionsAttr()
positions_attr.Set(points)

scales = [random_scale() for _ in range(num_particles)]
scale_attr = instancer.CreateScalesAttr()
scale_attr.Set(scales)


# Set the Instanced Geometry
instancer.CreatePrototypesRel().SetTargets([cube.GetPath()])
proto_attr = instancer.CreateProtoIndicesAttr()
# if we had more than a cube this would be the index into the list of geometries
# only use 0 here
proto_attr.Set([0] * num_particles, time=0)
# Orientation is a local orientation for each instance based on a half Quaternion
orientation = instancer.CreateOrientationsAttr()
rotations = [
    Gf.Quath(Gf.Rotation(Gf.Vec3d(1, 1, 1), random.uniform(0, 360)).GetQuat())
    for _ in range(num_particles)
]
orientation.Set(rotations, time=0)


# # create primvar colours for each instance
colors = [
    Gf.Vec3f(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    for _ in range(num_particles)
]
primvar_api = UsdGeom.PrimvarsAPI(instancer)
primvar = primvar_api.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray)
primvar.Set(colors)
primvar.SetInterpolation(UsdGeom.Tokens.vertex)

# negate so we can point to the 0,0,0 origin
directions = [-p for p in points]

# now run the Normalize function on each point not you can use list expression to do this
# as the normalize function also returns a float value
for i in range(len(directions)):
    directions[i].Normalize()

directions = [p * random.uniform(0.01, 0.1) for p in directions]

# now calculate p+dir for each of the points and directions
new_points = [p + d for p, d in zip(points, directions)]

for frame in range(1, num_frames):
    positions_attr.Set(new_points, time=frame)
    new_points = [p + d for p, d in zip(new_points, directions)]
    for i in range(len(rotations)):
        # update each current rotation by a small amount
        rotations[i] *= Gf.Quath(Gf.Rotation(Gf.Vec3d(1, 1, 1), 5.0).GetQuat())

    orientation.Set(rotations, time=frame)
# Print out the stage

# Save the resulting layer
stage.Export("pointsInstanced.usdc", addSourceFileComment=True)
