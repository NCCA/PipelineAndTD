#!/usr/bin/env python
from pxr import Usd, UsdGeom,Sdf

stage = Usd.Stage.Open('Mug.usda')

default_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/CoffeeCup"))
stage.SetDefaultPrim(default_prim.GetPrim())

# Clear local opinion, which always wins over variants.
colorAttr = UsdGeom.Gprim.Get(stage, '/CoffeeCup').GetDisplayColorAttr()
colorAttr.Clear()


# Create variant set.
rootPrim = stage.GetPrimAtPath('/CoffeeCup')
vset = rootPrim.GetVariantSets().AddVariantSet('shadingVariant')



# Create variant options.
vset.AddVariant('red')
vset.AddVariant('blue')
vset.AddVariant('green')



# Author red color behind red variant.
vset.SetVariantSelection('red')
with vset.GetVariantEditContext():
    colorAttr.Set([(1,0,0)])

vset.SetVariantSelection('blue')

with vset.GetVariantEditContext():
    colorAttr.Set([(0,0,1)])

vset.SetVariantSelection('green')
with vset.GetVariantEditContext():
    colorAttr.Set([(0,1,0)])

# now add size variants
vset = rootPrim.GetVariantSets().AddVariantSet('sizeVariant')
vset.AddVariant('default')

vset.AddVariant('small')
vset.AddVariant('medium')
vset.AddVariant('large')



vset.SetVariantSelection('small')
with vset.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0, 1.0, 0))
    xformable.AddScaleOp().Set((0.5, 0.5, 0.5))

vset.SetVariantSelection('medium')
with vset.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0, 1.5, 0))
    xformable.AddScaleOp().Set((1.5, 1.5, 1.5))


vset.SetVariantSelection('large')
with vset.GetVariantEditContext():
    xformable = UsdGeom.Xformable(rootPrim)
    xformable.AddTranslateOp().Set((0, 2.5, 0))
    xformable.AddScaleOp().Set((2.5, 2.5, 2.5))



stage.GetRootLayer().Export('MugWithVariants.usda')

# Print composed results-- note that variants get flattened away.
