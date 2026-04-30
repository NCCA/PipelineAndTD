import maya.api.OpenMaya as om2
import maya.cmds as cmds

it = om2.MItDag(om2.MItDag.kBreadthFirst)
node_fn = om2.MFnDagNode()
count = 0

while not it.isDone():
    obj = it.currentItem()

    if node_fn.has_object_type(obj, om2.MFn.kNamedObject):
        node_fn.set_object(obj)

        om2.MGlobal.displayInfo(f"ObjectName {node_fn.name()} Type {node_fn.type_name()}")
        om2.MGlobal.displayInfo(f"fullPathName {node_fn.full_path_name()}")
        om2.MGlobal.displayInfo(f"partialPathName {node_fn.partial_path_name()}")
        om2.MGlobal.displayInfo(f"Parent namespace {node_fn.parent_namespace()}")

        num_children = obj.num_children
        num_parents = node_fn.parent_count
        om2.MGlobal.displayInfo(f"number of children={num_children} number of parents={num_parents}")

        om2.MGlobal.displayInfo(f"attribute count = {node_fn.attribute_count}")
        om2.MGlobal.displayInfo("Transformation Matrix")

        m = node_fn.transformation_matrix
        om2.MGlobal.displayInfo(f"[{m(0, 0)},{m(0, 1)},{m(0, 2)},{m(0, 3)}]")
        om2.MGlobal.displayInfo(f"[{m(1, 0)},{m(1, 1)},{m(1, 2)},{m(1, 3)}]")
        om2.MGlobal.displayInfo(f"[{m(2, 0)},{m(2, 1)},{m(2, 2)},{m(2, 3)}]")
        om2.MGlobal.displayInfo(f"[{m(3, 0)},{m(3, 1)},{m(3, 2)},{m(3, 3)}]")
        om2.MGlobal.displayInfo("*" * 65)

    it.next()
    count += 1

om2.MGlobal.displayInfo(f"found {count} objects")
