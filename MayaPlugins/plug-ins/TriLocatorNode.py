"""
TriLocatorNode - Python API 2.0 port of the C++ TriLocatorNode plugin.

Draws a simple triangle locator in the viewport using Viewport 2.0 draw
override. The triangle has per-vertex colours (red, green, blue) and is
rendered as a filled mesh when shaded and as a line strip in wireframe.

Usage:
    Load the plugin in Maya, then create the node:
        cmds.createNode("TriLocatorNode")
"""

import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui

# Required for Maya to recognise this as an API 2.0 plugin
maya_useNewAPI = True

# ---------------------------------------------------------------------------
# Triangle geometry constants
# ---------------------------------------------------------------------------
#       V2 (0.0, 0.5, 0.0)
#
#  V1 (-0.5, -0.5, 0.0)    V3 (0.5, -0.5, 0.0)

SCALE = 0.5
TRIANGLE_VERTICES = [
    (-SCALE, -SCALE, 0.0),
    (0.0, SCALE, 0.0),
    (SCALE, -SCALE, 0.0),
]


# ---------------------------------------------------------------------------
# Draw data cache
# ---------------------------------------------------------------------------
class TriLocatorNodeData(om.MUserData):
    """Cached draw data passed from prepareForDraw to addUIDrawables."""

    def __init__(self):
        # False = Maya should NOT delete this after draw
        super().__init__(False)
        self.line_array = om.MPointArray()
        self.triangle_array = om.MPointArray()
        self.normal_array = om.MVectorArray()
        self.colour_array = om.MColorArray()


# ---------------------------------------------------------------------------
# Locator node
# ---------------------------------------------------------------------------
class TriLocatorNode(omui.MPxLocatorNode):
    """MPxLocatorNode subclass that provides bounding-box information
    and a size attribute controlling the triangle scale."""

    type_id = om.MTypeId(0x8001C)
    draw_db_classification = "drawdb/geometry/TriLocator"
    draw_registrant_id = "TriManipPlugin"

    # Attribute handle (set during initialize)
    size = None

    @classmethod
    def creator(cls):
        return cls()

    @staticmethod
    def initialize():
        unit_attr = om.MFnUnitAttribute()
        TriLocatorNode.size = unit_attr.create("size", "sz", om.MFnUnitAttribute.kDistance)
        unit_attr.default = om.MDistance(1.0)
        unit_attr.storable = True
        unit_attr.writable = True

        TriLocatorNode.addAttribute(TriLocatorNode.size)

    def compute(self, plug, data_block):
        return None  # Nothing to compute; equivalent to kUnknownParameter

    def isBounded(self):
        return True

    def boundingBox(self):
        this_node = self.thisMObject()
        plug = om.MPlug(this_node, TriLocatorNode.size)
        multiplier = plug.asMDistance().asCentimeters()

        corner1 = om.MPoint(-SCALE * multiplier, SCALE * multiplier, 0.0)
        corner2 = om.MPoint(SCALE * multiplier, -SCALE * multiplier, 0.0)
        return om.MBoundingBox(corner1, corner2)


# ---------------------------------------------------------------------------
# Viewport 2.0 draw override
# ---------------------------------------------------------------------------
class TriLocatorNodeDrawOverride(omr.MPxDrawOverride):
    """Handles all Viewport 2.0 drawing for TriLocatorNode."""

    # ------------------------------------------------------------------
    # Construction / destruction
    # ------------------------------------------------------------------
    def __init__(self, obj):
        # isAlwaysDirty=False for better performance; we manually mark
        # dirty via the modelEditorChanged callback.
        super().__init__(obj, None, False)
        self._locator_obj = obj
        self._current_bbox = om.MBoundingBox()
        self._model_editor_changed_cb = om.MEventMessage.addEventCallback(
            "modelEditorChanged", self._on_model_editor_changed
        )

    def __del__(self):
        if self._model_editor_changed_cb is not None:
            om.MMessage.removeCallback(self._model_editor_changed_cb)
            self._model_editor_changed_cb = None

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------
    def _on_model_editor_changed(self, *args):
        """Mark geometry dirty so it redraws on display-mode changes
        (e.g. wireframe <-> shaded)."""
        omr.MRenderer.setGeometryDrawDirty(self._locator_obj)

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------
    @staticmethod
    def creator(obj):
        return TriLocatorNodeDrawOverride(obj)

    # ------------------------------------------------------------------
    # Draw API support
    # ------------------------------------------------------------------
    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices

    # ------------------------------------------------------------------
    # Size attribute helper
    # ------------------------------------------------------------------
    @staticmethod
    def _get_multiplier(obj_path):
        """Read the size attribute value from the DAG node."""
        node = obj_path.node()
        plug = om.MPlug(node, TriLocatorNode.size)
        if not plug.isNull:
            return plug.asMDistance().asCentimeters()
        return 1.0

    # ------------------------------------------------------------------
    # Bounding box
    # ------------------------------------------------------------------
    def isBounded(self, obj_path, camera_path):
        return True

    def boundingBox(self, obj_path, camera_path):
        multiplier = self._get_multiplier(obj_path)
        corner1 = om.MPoint(-SCALE * multiplier, SCALE * multiplier, 0.0)
        corner2 = om.MPoint(SCALE * multiplier, -SCALE * multiplier, 0.0)
        self._current_bbox.clear()
        self._current_bbox.expand(corner1)
        self._current_bbox.expand(corner2)
        return self._current_bbox

    def disableInternalBoundingBoxDraw(self):
        return False

    # ------------------------------------------------------------------
    # Draw preparation
    # ------------------------------------------------------------------
    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        data = old_data
        if not isinstance(data, TriLocatorNodeData):
            data = TriLocatorNodeData()

        multiplier = self._get_multiplier(obj_path)

        # Build scaled vertices
        v = [
            om.MPoint(
                TRIANGLE_VERTICES[i][0] * multiplier,
                TRIANGLE_VERTICES[i][1] * multiplier,
                TRIANGLE_VERTICES[i][2] * multiplier,
            )
            for i in range(3)
        ]

        # Wireframe line segments: V0-V1, V1-V2, V2-V0
        data.line_array.clear()
        data.line_array.append(v[0])
        data.line_array.append(v[1])
        data.line_array.append(v[1])
        data.line_array.append(v[2])
        data.line_array.append(v[2])
        data.line_array.append(v[0])

        # Solid triangle
        data.triangle_array.clear()
        data.triangle_array.append(v[0])
        data.triangle_array.append(v[1])
        data.triangle_array.append(v[2])

        # Per-vertex normals (all facing +Z)
        normal = om.MVector(0.0, 0.0, 1.0)
        data.normal_array.clear()
        data.normal_array.append(normal)
        data.normal_array.append(normal)
        data.normal_array.append(normal)

        # Per-vertex colours: red, green, blue
        data.colour_array.clear()
        data.colour_array.append(om.MColor((1.0, 0.0, 0.0)))
        data.colour_array.append(om.MColor((0.0, 1.0, 0.0)))
        data.colour_array.append(om.MColor((0.0, 0.0, 1.0)))

        return data

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        if not isinstance(data, TriLocatorNodeData):
            return

        draw_manager.beginDrawable()
        draw_manager.setDepthPriority(5)

        # Draw filled triangle when in shaded display mode
        if frame_context.getDisplayStyle() & omr.MFrameContext.kGouraudShaded:
            draw_manager.mesh(
                omr.MUIDrawManager.kTriangles,
                data.triangle_array,
                data.normal_array,
                data.colour_array,
            )

        # Always draw wireframe outline
        draw_manager.mesh(
            omr.MUIDrawManager.kLineStrip,
            data.line_array,
            data.normal_array,
            data.colour_array,
        )

        draw_manager.endDrawable()


# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "NCCA", "1.0", "Any")

    plugin.registerNode(
        "TriLocatorNode",
        TriLocatorNode.type_id,
        TriLocatorNode.creator,
        TriLocatorNode.initialize,
        om.MPxNode.kLocatorNode,
        TriLocatorNode.draw_db_classification,
    )

    omr.MDrawRegistry.registerDrawOverrideCreator(
        TriLocatorNode.draw_db_classification,
        TriLocatorNode.draw_registrant_id,
        TriLocatorNodeDrawOverride.creator,
    )


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    omr.MDrawRegistry.deregisterDrawOverrideCreator(
        TriLocatorNode.draw_db_classification,
        TriLocatorNode.draw_registrant_id,
    )

    plugin.deregisterNode(TriLocatorNode.type_id)
