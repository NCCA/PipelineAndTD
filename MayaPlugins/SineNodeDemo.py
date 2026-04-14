import maya.cmds as cmds

cmds.createNode("SineNodePy")
cmds.connectAttr("time1.outTime", "SineNodePy1.time")
cmds.polySphere()
cmds.connectAttr("SineNodePy1.o", "pSphere1.tx")
cmds.connectAttr("SineNodePy1.o", "pSphere1.ty")
cmds.select("SineNodePy1")
