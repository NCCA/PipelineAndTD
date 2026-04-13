"""
CubeLocatorNode - Python API 2.0 locator plugin.

Draws a box locator in the viewport using Viewport 2.0 draw override.
The box dimensions are controlled by width, height and depth attributes.
A derived volume attribute is computed from those three inputs.
A colour attribute drives the single draw colour for both wireframe and
solid display modes.

Usage:
    Load the plugin in Maya, then create the node:
        cmds.createNode("CubeLocatorNode")

    Query the computed volume:
        cmds.getAttr("cubeLocatorNode1.volume")
"""

import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui

ATTRIBUTE_CATEGORY = "Cube Locator"
# Required for Maya to recognise this as an API 2.0 plugin
maya_useNewAPI = True

# ---------------------------------------------------------------------------
# Cube geometry helpers
# ---------------------------------------------------------------------------
#  The cube is centred at the origin.  Vertices are labelled:
#
#     6 ---- 7
#    /|      /|
#   2 ---- 3  |
#   |  4 --|--5
#   | /    | /
#   0 ---- 1
#
#  v0 = (-w/2, -h/2, -d/2)   v4 = (-w/2, -h/2, +d/2)
#  v1 = (+w/2, -h/2, -d/2)   v5 = (+w/2, -h/2, +d/2)
#  v2 = (-w/2, +h/2, -d/2)   v6 = (-w/2, +h/2, +d/2)
#  v3 = (+w/2, +h/2, -d/2)   v7 = (+w/2, +h/2, +d/2)

# Each face is two counter-clockwise triangles (viewed from outside).
# (vertex-index-triple, outward normal)
_FACE_TRIS = [
    # front  (+Z)
    ([4, 5, 6], (0.0, 0.0, 1.0)),
    ([5, 7, 6], (0.0, 0.0, 1.0)),
    # back   (-Z)
    ([1, 0, 3], (0.0, 0.0, -1.0)),
    ([0, 2, 3], (0.0, 0.0, -1.0)),
    # right  (+X)
    ([1, 3, 5], (1.0, 0.0, 0.0)),
    ([5, 3, 7], (1.0, 0.0, 0.0)),
    # left   (-X)
    ([4, 6, 0], (-1.0, 0.0, 0.0)),
    ([0, 6, 2], (-1.0, 0.0, 0.0)),
    # top    (+Y)
    ([2, 6, 3], (0.0, 1.0, 0.0)),
    ([3, 6, 7], (0.0, 1.0, 0.0)),
    # bottom (-Y)
    ([0, 1, 4], (0.0, -1.0, 0.0)),
    ([1, 5, 4], (0.0, -1.0, 0.0)),
]

# 12 unique edges expressed as index pairs into the 8-vertex list
_EDGES = [
    (0, 1),
    (1, 3),
    (3, 2),
    (2, 0),  # back face loop
    (4, 5),
    (5, 7),
    (7, 6),
    (6, 4),  # front face loop
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),  # connecting edges
]


def _build_cube_verts(w, h, d):
    """Return the 8 corner MPoints for a cube of the given dimensions."""
    hw, hh, hd = w * 0.5, h * 0.5, d * 0.5
    return [
        om.MPoint(-hw, -hh, -hd),  # 0
        om.MPoint(hw, -hh, -hd),  # 1
        om.MPoint(-hw, hh, -hd),  # 2
        om.MPoint(hw, hh, -hd),  # 3
        om.MPoint(-hw, -hh, hd),  # 4
        om.MPoint(hw, -hh, hd),  # 5
        om.MPoint(-hw, hh, hd),  # 6
        om.MPoint(hw, hh, hd),  # 7
    ]


# ---------------------------------------------------------------------------
# Draw data cache
# ---------------------------------------------------------------------------
class CubeLocatorNodeData(om.MUserData):
    """Cached draw data passed from prepareForDraw to addUIDrawables."""

    def __init__(self):
        # False = Maya should NOT delete this after draw
        super().__init__(False)
        self.line_array = om.MPointArray()
        self.triangle_array = om.MPointArray()
        self.normal_array = om.MVectorArray()
        self.colour = om.MColor((1.0, 1.0, 1.0, 1.0))
        self.text_colour = om.MColor((1.0, 1.0, 1.0, 1.0))
        self.label = ""
        self.volume_text = ""
        self.center = om.MPoint()


# ---------------------------------------------------------------------------
# Locator node
# ---------------------------------------------------------------------------
class CubeLocatorNode(omui.MPxLocatorNode):
    """MPxLocatorNode that draws a resizable, coloured box.

    Attributes
    ----------
    width, height, depth : MFnUnitAttribute (kDistance)
        Dimensions of the box.
    volume : MFnNumericAttribute (kDouble, output)
        Computed as width * height * depth (in centimetres).
    colour : MFnNumericAttribute (k3Float / colour)
        RGB colour used for drawing.
    """

    type_id = om.MTypeId(0x8001D)
    draw_db_classification = "drawdb/geometry/CubeLocator"
    draw_registrant_id = "CubeLocatorPlugin"

    # Attribute handles (populated in initialize)
    width = None
    height = None
    depth = None
    volume = None
    colour = None
    textColour = None

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    @classmethod
    def creator(cls):
        return cls()

    def postConstructor(self):
        print("post constructor called")
        fn = om.MFnDependencyNode(self.thisMObject())
        fn.setName("cubeLocatorNodeShape#")

    # ------------------------------------------------------------------
    # Attribute factory helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _make_distance(name, short, default_cm=1.0):
        fn = om.MFnUnitAttribute()
        attr = fn.create(name, short, om.MFnUnitAttribute.kDistance)
        fn.default = om.MDistance(default_cm)
        fn.storable = True
        fn.writable = True
        fn.keyable = True
        fn.addToCategory(ATTRIBUTE_CATEGORY)
        CubeLocatorNode.addAttribute(attr)
        return attr

    @staticmethod
    def _make_double_output(name, short):
        fn = om.MFnNumericAttribute()
        attr = fn.create(name, short, om.MFnNumericData.kDouble, 0.0)
        fn.storable = False
        fn.writable = False
        fn.readable = True
        fn.cached = False
        fn.addToCategory(ATTRIBUTE_CATEGORY)
        CubeLocatorNode.addAttribute(attr)
        return attr

    @staticmethod
    def _make_color(name, short, default=(1.0, 1.0, 1.0)):
        fn = om.MFnNumericAttribute()
        attr = fn.createColor(name, short)
        fn.default = default
        fn.storable = True
        fn.writable = True
        fn.keyable = False
        fn.channelBox = True
        fn.addToCategory(ATTRIBUTE_CATEGORY)
        CubeLocatorNode.addAttribute(attr)
        return attr

    # ------------------------------------------------------------------
    @staticmethod
    def initialize():
        CubeLocatorNode.width = CubeLocatorNode._make_distance("width", "w")
        CubeLocatorNode.height = CubeLocatorNode._make_distance("height", "h")
        CubeLocatorNode.depth = CubeLocatorNode._make_distance("depth", "dp")

        CubeLocatorNode.volume = CubeLocatorNode._make_double_output("volume", "vol")

        CubeLocatorNode.colour = CubeLocatorNode._make_color("colour", "col")
        CubeLocatorNode.textColour = CubeLocatorNode._make_color("textColour", "tc", (1.0, 1.0, 1.0))

        # --- dependency graph connections ---
        CubeLocatorNode.attributeAffects(CubeLocatorNode.width, CubeLocatorNode.volume)
        CubeLocatorNode.attributeAffects(CubeLocatorNode.height, CubeLocatorNode.volume)
        CubeLocatorNode.attributeAffects(CubeLocatorNode.depth, CubeLocatorNode.volume)

    # ------------------------------------------------------------------
    def compute(self, plug, data_block):
        if plug != CubeLocatorNode.volume:
            return None  # kUnknownParameter equivalent

        w = data_block.inputValue(CubeLocatorNode.width).asDistance().asCentimeters()
        h = data_block.inputValue(CubeLocatorNode.height).asDistance().asCentimeters()
        d = data_block.inputValue(CubeLocatorNode.depth).asDistance().asCentimeters()

        vol_handle = data_block.outputValue(CubeLocatorNode.volume)
        vol_handle.setDouble(w * h * d)
        data_block.setClean(plug)
        return None

    # ------------------------------------------------------------------
    def isBounded(self):
        return True

    def boundingBox(self):
        node = self.thisMObject()
        w = om.MPlug(node, CubeLocatorNode.width).asMDistance().asCentimeters()
        h = om.MPlug(node, CubeLocatorNode.height).asMDistance().asCentimeters()
        d = om.MPlug(node, CubeLocatorNode.depth).asMDistance().asCentimeters()

        hw, hh, hd = w * 0.5, h * 0.5, d * 0.5
        return om.MBoundingBox(
            om.MPoint(-hw, -hh, -hd),
            om.MPoint(hw, hh, hd),
        )


# ---------------------------------------------------------------------------
# Viewport 2.0 draw override
# ---------------------------------------------------------------------------
class CubeLocatorNodeDrawOverride(omr.MPxDrawOverride):
    """Handles all Viewport 2.0 drawing for CubeLocatorNode."""

    # ------------------------------------------------------------------
    def __init__(self, obj):
        # isAlwaysDirty=False; we mark dirty via callback instead
        super().__init__(obj, None, False)
        self._locator_obj = obj
        self._current_bbox = om.MBoundingBox()
        self._model_editor_changed_cb = om.MEventMessage.addEventCallback(
            "modelEditorChanged", self._on_model_editor_changed
        )

    def __del__(self):
        # Guard against the Maya API being partially torn down during plugin
        # unload, which can cause MMessage.removeCallback to crash.
        try:
            if self._model_editor_changed_cb is not None:
                om.MMessage.removeCallback(self._model_editor_changed_cb)
                self._model_editor_changed_cb = None
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _on_model_editor_changed(self, *args):
        # The node may have been deleted (file new / scene clear) before the
        # draw override is destroyed.  Calling setGeometryDrawDirty with an
        # invalid MObject crashes Maya, so check validity first.
        if self._locator_obj is not None and not self._locator_obj.isNull():
            omr.MRenderer.setGeometryDrawDirty(self._locator_obj)

    # ------------------------------------------------------------------
    @staticmethod
    def creator(obj):
        return CubeLocatorNodeDrawOverride(obj)

    # ------------------------------------------------------------------
    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices

    # ------------------------------------------------------------------
    @staticmethod
    def _get_dimensions(obj_path):
        """Return (width, height, depth) in centimetres from the DAG node."""
        node = obj_path.node()

        def _cm(attr):
            plug = om.MPlug(node, attr)
            return plug.asMDistance().asCentimeters() if not plug.isNull else 1.0

        return (
            _cm(CubeLocatorNode.width),
            _cm(CubeLocatorNode.height),
            _cm(CubeLocatorNode.depth),
        )

    @staticmethod
    def _get_colour(obj_path):
        """Return the colour attribute value as an MColor."""
        node = obj_path.node()
        plug = om.MPlug(node, CubeLocatorNode.colour)
        if plug.isNull:
            return om.MColor((1.0, 1.0, 1.0))
        r = plug.child(0).asFloat()
        g = plug.child(1).asFloat()
        b = plug.child(2).asFloat()
        return om.MColor((r, g, b, 1.0))

    @staticmethod
    def _get_text_colour(obj_path):
        """Return the textColour attribute value as an MColor."""
        node = obj_path.node()
        plug = om.MPlug(node, CubeLocatorNode.textColour)
        if plug.isNull:
            return om.MColor((1.0, 1.0, 1.0, 1.0))
        r = plug.child(0).asFloat()
        g = plug.child(1).asFloat()
        b = plug.child(2).asFloat()
        return om.MColor((r, g, b, 1.0))

    # ------------------------------------------------------------------
    def isBounded(self, obj_path, camera_path):
        return True

    def boundingBox(self, obj_path, camera_path):
        w, h, d = self._get_dimensions(obj_path)
        hw, hh, hd = w * 0.5, h * 0.5, d * 0.5
        self._current_bbox.clear()
        self._current_bbox.expand(om.MPoint(-hw, -hh, -hd))
        self._current_bbox.expand(om.MPoint(hw, hh, hd))
        return self._current_bbox

    def disableInternalBoundingBoxDraw(self):
        return False

    # ------------------------------------------------------------------
    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        data = old_data
        if not isinstance(data, CubeLocatorNodeData):
            data = CubeLocatorNodeData()

        w, h, d = self._get_dimensions(obj_path)
        verts = _build_cube_verts(w, h, d)

        # --- wireframe: one MPoint per endpoint of each edge (kLines) ---
        data.line_array.clear()
        for i, j in _EDGES:
            data.line_array.append(verts[i])
            data.line_array.append(verts[j])

        # --- solid: expanded triangle list with per-face normals ---
        data.colour = self._get_colour(obj_path)
        data.text_colour = self._get_text_colour(obj_path)
        data.label = obj_path.partialPathName()
        data.volume_text = f"{w * h * d:.2f}"
        data.center = om.MPoint(0.0, h * 0.5, 0.0)

        data.triangle_array.clear()
        data.normal_array.clear()
        for indices, nxyz in _FACE_TRIS:
            normal = om.MVector(*nxyz)
            for idx in indices:
                data.triangle_array.append(verts[idx])
                data.normal_array.append(normal)

        return data

    # ------------------------------------------------------------------
    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        if not isinstance(data, CubeLocatorNodeData):
            return

        draw_manager.beginDrawable()
        draw_manager.setDepthPriority(5)

        display_style = frame_context.getDisplayStyle()
        shaded = display_style & (omr.MFrameContext.kGouraudShaded | omr.MFrameContext.kFlatShaded)

        # Filled faces in any shaded display mode using a single flat colour.
        if shaded:
            draw_manager.setColor(data.colour)
            draw_manager.mesh(
                omr.MUIDrawManager.kTriangles,
                data.triangle_array,
                data.normal_array,
            )

        # Wireframe edges: always in wireframe mode, and as an overlay when
        # "Wireframe on Shaded" is active alongside a shaded mode.
        if (not shaded) or (display_style & omr.MFrameContext.kWireFrame):
            draw_manager.setColor(data.colour)
            draw_manager.mesh(
                omr.MUIDrawManager.kLines,
                data.line_array,
            )

        draw_manager.setColor(data.text_colour)
        draw_manager.setFontSize(omr.MUIDrawManager.kSmallFontSize)
        pos_label = om.MPoint(data.center.x, data.center.y + 0.15, data.center.z)
        draw_manager.text(pos_label, f"{data.label} ({data.volume_text})", omr.MUIDrawManager.kCenter)

        draw_manager.endDrawable()


# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "NCCA", "1.0", "Any")

    plugin.registerNode(
        "CubeLocatorNode",
        CubeLocatorNode.type_id,
        CubeLocatorNode.creator,
        CubeLocatorNode.initialize,
        om.MPxNode.kLocatorNode,
        CubeLocatorNode.draw_db_classification,
    )

    omr.MDrawRegistry.registerDrawOverrideCreator(
        CubeLocatorNode.draw_db_classification,
        CubeLocatorNode.draw_registrant_id,
        CubeLocatorNodeDrawOverride.creator,
    )


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    omr.MDrawRegistry.deregisterDrawOverrideCreator(
        CubeLocatorNode.draw_db_classification,
        CubeLocatorNode.draw_registrant_id,
    )

    plugin.deregisterNode(CubeLocatorNode.type_id)
