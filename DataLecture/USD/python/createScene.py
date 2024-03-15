#!/usr/bin/env python
from pxr import Sdf, Usd, UsdGeom


def add_sub_layer(sub_layer_path: str, root_layer) -> Sdf.Layer:
    sub_layer: Sdf.Layer = Sdf.Layer.CreateNew(sub_layer_path)
    # You can use standard python list.insert to add the subLayer to any position in the list
    root_layer.subLayerPaths.append(sub_layer.identifier)
    return sub_layer


# Open a stage for writing
stage = Usd.Stage.CreateNew("layer-cube.usda")

# Add the sub layer to the root layer
root = stage.GetRootLayer()
add_sub_layer("./blue-cube.usda", root)
add_sub_layer("./cube.usda", root)


# Print out the stage
print(stage.GetRootLayer().ExportToString())

# Save the resulting layer
# stage.Export("layer-cube.usda", addSourceFileComment=False)
stage.GetRootLayer().Save()
