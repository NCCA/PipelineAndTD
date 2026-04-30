import random

import maya.api.OpenMaya as OM
import maya.cmds as cmds


def random_move():
    cmds.move(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))


def generate_scene():
    cmds.polyCube()
    random_move()
    cmds.polySphere()
    random_move()
    cmds.polyCone()
    random_move()
    cmds.polyTorus()
    random_move()
    cmds.select(cmds.ls(type="mesh"))


cmds.select(cmds.ls(type="mesh"))
cmds.delete()
generate_scene()
node_fn = OM.MFnDagNode()
list = OM.MGlobal.getActiveSelectionList()
for i in range(0, list.length()):
    path = list.getDagPath(i)
    node_fn.setObject(path)
    print(f"Object {node_fn.name()} is selected")


dagIt = OM.MItDag(OM.MItDag.kBreadthFirst)
while not dagIt.isDone():
    node = dagIt.currentItem()
    node_fn.setObject(node)
    if node.hasFn(OM.MFn.kNamedObject):
        print(f"Object {node_fn.name()} type {node_fn.typeName}")
        m = node_fn.transformationMatrix()
        print(m)
    dagIt.next()
