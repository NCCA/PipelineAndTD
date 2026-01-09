#!/usr/bin/env -S uv run --script
from pxr import Sdf, Usd, UsdGeom

# Create a temporary stage in memory
stage = Usd.Stage.CreateInMemory("stage.usda")

# Override the world as a prim
world = stage.OverridePrim("/World")
cube = stage.OverridePrim("/World/Cube")
prim = UsdGeom.Gprim(cube)
prim.CreateDisplayColorAttr([(0.0, 0.0, 1.0)])
xformable = UsdGeom.Xformable(cube)

xformable.AddRotateXYZOp().Set((45.0, 45.0, 0.0))

# Print out the stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
stage.Export("blue-cube.usda", addSourceFileComment=False)
