import maya.cmds as cmds


def update_mesh():
    nVerts = cmds.polyEvaluate("pPlane1", v=True)
    for i in range(0, nVerts):
        a = cmds.pointPosition("pPlane1.vtx[%d]" % i)
        cmds.setAttr("NoiseNode1.positionX", a[0])
        cmds.setAttr("NoiseNode1.positionZ", a[2])
        pos = cmds.getAttr("NoiseNode1.position")
        o = cmds.getAttr("NoiseNode1.output")
        cmds.xform("pPlane1.vtx[%d]" % i, a=True, ws=True, t=(a[0], o, a[2]))


cmds.file(new=True, force=True)
loaded = cmds.pluginInfo(query=True, listPlugins=True)


if "NoiseNode" in loaded:
    cmds.unloadPlugin("NoiseNode.py", force=True)

cmds.polyPlane(w=42, h=42, sx=80, sy=80)
cmds.loadPlugin("NoiseNode.py")
cmds.createNode("NoiseNode")
cmds.select("NoiseNode1")
cmds.setAttr("NoiseNode1.scale", 4)
cmds.setAttr("NoiseNode1.amplitude", 9)
cmds.setAttr("NoiseNode1.noise_type", 0)

update_mesh()
