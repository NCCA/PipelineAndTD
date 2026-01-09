#!/usr/bin/env -S uv run --script
from pxr import Sdf, Usd, UsdGeom

stage = Usd.Stage.Open("Mug.usda")

default_prim = UsdGeom.Mesh.Define(stage, Sdf.Path("/CoffeeCup"))
stage.SetDefaultPrim(default_prim.GetPrim())

# Clear local opinion, which always wins over variants.
colorAttr = UsdGeom.Gprim.Get(stage, "/CoffeeCup").GetDisplayColorAttr()
colorAttr.Clear()


# Create variant set.
rootPrim = stage.GetPrimAtPath("/CoffeeCup")
variant_set = rootPrim.GetVariantSets().AddVariantSet("shadingVariant")

# Create variant options.
variant_set.AddVariant("red")
variant_set.AddVariant("blue")
variant_set.AddVariant("green")


# Author red color behind red variant.
variant_set.SetVariantSelection("red")
with variant_set.GetVariantEditContext():
    colorAttr.Set([(1, 0, 0)])

variant_set.SetVariantSelection("blue")

with variant_set.GetVariantEditContext():
    colorAttr.Set([(0, 0, 1)])

variant_set.SetVariantSelection("green")
with variant_set.GetVariantEditContext():
    colorAttr.Set([(0, 1, 0)])

# now add size variants
variant_set = rootPrim.GetVariantSets().AddVariantSet("sizeVariant")
variant_set.AddVariant("default")
variant_set.AddVariant("small")
variant_set.AddVariant("medium")
variant_set.AddVariant("large")

variant_set.SetVariantSelection("default")
with variant_set.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0.0, 1.1, 0.0))
    xformable.AddScaleOp().Set((0.2, 0.2, 0.2))


variant_set.SetVariantSelection("small")
with variant_set.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0.0, 0.7, 0.0))
    xformable.AddScaleOp().Set((0.1, 0.1, 0.1))

variant_set.SetVariantSelection("medium")
with variant_set.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0.0, 1.6, 0.0))
    xformable.AddScaleOp().Set((0.3, 0.3, 0.3))


variant_set.SetVariantSelection("large")
with variant_set.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0.0, 2.2, 0.0))
    xformable.AddScaleOp().Set((0.4, 0.4, 0.4))


stage.GetRootLayer().Export("MugWithVariants.usda")

# Print composed results-- note that variants get flattened away.
