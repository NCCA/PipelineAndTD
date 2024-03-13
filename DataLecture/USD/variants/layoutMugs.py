#!/usr/bin/env python
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade
import random
def _addGround(stage, width, depth):
    boxPrim = UsdGeom.Mesh.Define(stage, "/World/Cube")
    boxPrim.CreatePointsAttr().Set([(-width, 0, depth), (width, 0 ,depth), (width, 0, -depth), (-width, 0, -depth) ]) 
    boxPrim.CreateFaceVertexCountsAttr().Set([4])
    boxPrim.CreateFaceVertexIndicesAttr().Set([0, 1, 2,3])
    boxPrim.CreateExtentAttr().Set([(-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)])
    boxPrim.CreateNormalsAttr().Set([(0, 0, 1)])

    # boxPrim = UsdGeom.Cube.Define(stage, "/World/ground")
    # boxPrim.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])
    # xformable = UsdGeom.Xformable(boxPrim)
    # xformable.AddScaleOp().Set(Gf.Vec3f(width, 0.1, depth))

    mtl_path = Sdf.Path("/World/GroundMaterial")
    mtl = UsdShade.Material.Define(stage, mtl_path)
    shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("Shader"))
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 1.0, 1.0))
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.5)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    mtl.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")
    boxPrim.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
    UsdShade.MaterialBindingAPI(boxPrim).Bind(mtl)


    UsdShade.MaterialBindingAPI(boxPrim).Bind(mtl)


def _addCamera(stage):
    cam = UsdGeom.Camera.Define(stage, "/World/main_cam")

    # the camera derives from UsdGeom.Xformable so we can
    # use the XformCommonAPI on it, too, and see how rotations are handled
    xformAPI = UsdGeom.XformCommonAPI(cam)
    xformAPI.SetTranslate((8, 1.8, 8))
    # -86 degree rotation around X axis.  Can specify rotation order as
    # optional parameter
    xformAPI.SetRotate((-10, 0, 0))


def _add_payload(prim: Usd.Prim, payload_asset_path: str, payload_target_path: Sdf.Path) -> None:
    #payloads: Usd.Payloads = prim.GetPayloads()
    references: Usd.References = prim.GetReferences()
    references.AddReference(
        assetPath=payload_asset_path,
        #primPath=payload_target_path # OPTIONAL: Payload a specific target prim. Otherwise, uses the payloadd layer's defaultPrim.
    )




def _createMugs(stage, width, depth):
    payload_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World/CoffeeCup00")).GetPrim()
    # now load the file MugWithVariants.usda and place in scene
    _add_payload(payload_prim, r"./MugWithVariants.usda", Sdf.Path.emptyPath)
    # # Now make visible
    # prim = stage.GetPrimAtPath("/World/CoffeeCup00")
    # visibility_attribute = prim.GetAttribute("visibility")
    # visibility_attribute.Set("visible")
    colours=["red","green","blue"]
    sizes=["default","small","medium","large"]
    primNumber=0
    for i in range(-20,20,4):
        for j in range(-20,20,4):
            ## now add the payload
            path=Sdf.Path(f"/World/CoffeeCup{primNumber}")
            primNumber+=1
            payload_prim = UsdGeom.Mesh.Define(stage,path ).GetPrim()
            _add_payload(payload_prim, r"./MugWithVariants.usda", Sdf.Path.emptyPath)
            mug=stage.GetPrimAtPath(path)

            # Set variant for colour
            variant_set = mug.GetVariantSets().GetVariantSet("shadingVariant")
            variant_set.SetVariantSelection(random.choice(colours))

            variant_set = mug.GetVariantSets().GetVariantSet("sizeVariant")
            variant_set.SetVariantSelection(random.choice(sizes))
            xform = UsdGeom.Xformable(mug)
            local_transform = xform.GetLocalTransformation()
            translate = local_transform.ExtractTranslation()
            UsdGeom.XformCommonAPI(mug).SetTranslate((i,translate[1],j))




            # xformable = UsdGeom.Xformable(mug)
            # xformable.AddTranslateOp().Set((i, 0.5, j))
            # xformable.AddScaleOp().Set((0.5, 1.0, 0.5))
            


            # primPath = prototypesPrimPath.AppendChild("/World/CoffeeCup")
            # treeRefPrim = stage.DefinePrim(primPath)
            # refs = treeRefPrim.GetReferences()
            # refs.AddReference("/World/CoffeeCup")
            # mug.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])


def main():
    stage = Usd.Stage.CreateNew("MugScene.usda")
    world = UsdGeom.Xform.Define(stage, "/World")
   
    #_addCamera(stage)
    _addGround(stage, 30, 30)
    _createMugs(stage,10,10)


    stage.GetRootLayer().Save()


if __name__ == "__main__":
    main()
