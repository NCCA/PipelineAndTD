import maya.api.OpenMaya as om
import maya.cmds as cmds

dag_it = om.MItDag(om.MItDag.kBreadthFirst)
count = 0

om.MGlobal.displayInfo("traversing DAG")

while not dag_it.isDone():
    node = dag_it.currentItem()
    node_fn = om.MFnDagNode(node)

    if node.hasFn(om.MFn.kNamedObject):
        om.MGlobal.displayInfo("Object " + node_fn.name() + " type " + node_fn.typeName)
        om.MGlobal.displayInfo("fullPathName " + node_fn.fullPathName())
        om.MGlobal.displayInfo("partialPathName " + node_fn.partialPathName())
        om.MGlobal.displayInfo("Parent path " + node_fn.partialPathName())

        full_path = node_fn.fullPathName()
        namespace = cmds.ls(full_path, showNamespace=True)
        parent_ns = namespace[1] if namespace and len(namespace) > 1 else ":"
        om.MGlobal.displayInfo("Parent namespace " + parent_ns)

        om.MGlobal.displayInfo(
            f"number of children= {node_fn.childCount()} number of parents= {node_fn.parentCount()} "
        )
        om.MGlobal.displayInfo(f"attribute count = {node_fn.attributeCount()} ")

        om.MGlobal.displayInfo("Transformation Matrix")
        m = node_fn.transformationMatrix()

        # MMatrix in Python API 2.0 is a flat list of 16 floats — index as m[row * 4 + col]
        for row in range(4):
            c = row * 4
            om.MGlobal.displayInfo(f"[{m[c]},{m[c + 1]},{m[c + 2]},{m[c + 3]}]")

        om.MGlobal.displayInfo("*" * 69)
        count += 1

    dag_it.next()

om.MGlobal.displayInfo(f"found {count} objects")
