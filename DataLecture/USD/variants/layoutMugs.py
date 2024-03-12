#!/usr/bin/env python
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

def _addGround(stage, width, depth):
    boxPrim = UsdGeom.Cube.Define(stage, "/World/ground")
    boxPrim.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])
    xformable = UsdGeom.Xformable(boxPrim)
    xformable.AddScaleOp().Set(Gf.Vec3f(width, 0.1, depth))

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
    # Now make visible
    prim = stage.GetPrimAtPath("/World/CoffeeCup00")
    visibility_attribute = prim.GetAttribute("visibility")
    visibility_attribute.Set("visible")

    
    # for i in range(10):
    #     for j in range(10):
    #         ## now add the payload
    #         payload_prim = UsdGeom.Xform.Define(stage, Sdf.Path(f"/World/CoffeeCup{i}{j}")).GetPrim()
    #         _add_payload(payload_prim, r"./MugWithVariants.usda", Sdf.Path.emptyPath)
    #         #refs.AddReference("/CoffeeCup")
    #         #geo.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])
    #         #xformable = UsdGeom.Xformable(geo)
    #         #xformable.AddTranslateOp().Set((i, 0.5, j))
    #         #xformable.AddScaleOp().Set((0.5, 1.0, 0.5))
            


            # primPath = prototypesPrimPath.AppendChild("/World/CoffeeCup")
            # treeRefPrim = stage.DefinePrim(primPath)
            # refs = treeRefPrim.GetReferences()
            # refs.AddReference("/World/CoffeeCup")
            # mug.CreateDisplayColorAttr([(0.5, 0.2, 0.0)])
            # xformable = UsdGeom.Xformable(mug)
            # xformable.AddTranslateOp().Set((i, 0.5, j))
            # xformable.AddScaleOp().Set((0.5, 1.0, 0.5))


def main():
    stage = Usd.Stage.CreateNew("MugScene.usda")
    world = UsdGeom.Xform.Define(stage, "/World")
   
    #_addCamera(stage)
    #_addGround(stage, 10, 10)
    _createMugs(stage,10,10)


    stage.GetRootLayer().Save()


if __name__ == "__main__":
    main()
