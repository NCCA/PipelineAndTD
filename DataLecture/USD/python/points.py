#!/usr/bin/env python
from pxr import Usd, UsdGeom
import random
import math

def normalize(d) :
    s=math.sqrt(d[0]*d[0]+d[1]*d[1]+d[2]*d[2])
    return (-d[0]/s,-d[1]/s,-d[2])

def random_point(extents = 10) :
    return tuple( random.uniform(-extents,extents) for _ in range(3))


# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("points.usda")
stage.SetStartTimeCode(0)
stage.SetEndTimeCode(100)

# Create a transform and add a Cube as mesh data
xformPrim = UsdGeom.Xform.Define(stage, "/World")
stage.GetRootLayer().defaultPrim = 'World'   
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
# 1 unit == 1 meter
UsdGeom.SetStageMetersPerUnit(stage, 1.0) 

pointsPrim = UsdGeom.Points.Define(stage, "/World/PointSet1")
num_particles = 10000

points = [random_point() for _ in range(num_particles)]


pointsPrim.CreatePointsAttr().Set(points,time=0)

pointsPrim.CreateWidthsAttr().Set([0.01] * num_particles)
# create direction vectors
normalized_points = [normalize(point) for point in points]
new_points=[(points[p][0]* normalized_points[p][0],
                points[p][1]* normalized_points[p][1],
                points[p][2]* normalized_points[p][2]) 
            for p in range(num_particles)]

for frame in range(1,100) :
    
    pointsPrim.CreatePointsAttr().Set(new_points,time=frame)
    new_points=[(new_points[p][0]* normalized_points[p][0],
                 new_points[p][1]* normalized_points[p][1],
                 new_points[p][2]* normalized_points[p][2]) 
                for p in range(num_particles)]


# Print out the stage
#print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("points.usda", addSourceFileComment=True)