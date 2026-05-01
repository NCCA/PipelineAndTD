"""
RibExport - Maya Python plugin
Exports Maya scenes to RenderMan RIB format.
Original C++ code by Jon Macey, converted to Maya Python.

API NOTES - several classes do NOT exist in maya.api (2.0) and must use 1.0:
    Missing from API 2.0              Use instead
    --------------------------------  ----------------------------
    MPxFileTranslator                 maya.OpenMayaMPx
    MFnPlugin (for translators)       maya.OpenMayaMPx
    MCommonRenderSettingsData         maya.OpenMayaRender  (1.0)
    MRenderUtil                       maya.OpenMayaRender  (1.0)
    MFnLight / MFnSpotLight etc.      maya.OpenMaya        (1.0)
    MFnDirectionalLight               maya.OpenMaya        (1.0)
    MFnAmbientLight                   maya.OpenMaya        (1.0)

Everything else (mesh, camera, iterators, matrices) uses API 2.0.

Usage:
    Load via Maya's Plugin Manager, then:
        File > Export All  (file type "RibExport")
    Or via MEL:
        file -type "RibExport" -exportAll "path/to/output";

Option string format (semicolon-separated):
    "-normals=1;-uvs=1;-geo=1;-lights=1"
"""

import math
import sys

# ---------------------------------------------------------------------------
# API 2.0 – for everything that IS available (mesh, camera, iterators, etc.)
# ---------------------------------------------------------------------------
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2
import maya.cmds as cmds

# ---------------------------------------------------------------------------
# API 1.0 – for classes not yet ported to API 2.0
# ---------------------------------------------------------------------------
import maya.OpenMaya as om1
import maya.OpenMayaAnim as oma1
import maya.OpenMayaMPx as mpx
import maya.OpenMayaRender as omr  # MCommonRenderSettingsData, MRenderUtil

# ---------------------------------------------------------------------------
# Plugin metadata
# ---------------------------------------------------------------------------
PLUGIN_NAME = "RibExport"
PLUGIN_VERSION = "1.0"
PLUGIN_VENDOR = "Jon Macey"
OPTION_SCRIPT = "RibExportScript"
DEFAULT_OPTIONS = ""


# ===========================================================================
class RibExport(mpx.MPxFileTranslator):
    """Writes one RenderMan RIB file per frame over the Render Globals range."""

    # ------------------------------------------------------------------
    # MPxFileTranslator interface
    # ------------------------------------------------------------------
    def haveReadMethod(self):
        return False

    def haveWriteMethod(self):
        return True

    def defaultExtension(self):
        return "rib"

    def filter(self):
        return "*.rib"

    # ------------------------------------------------------------------
    # writer
    # ------------------------------------------------------------------
    def writer(self, file_object, options_string, access_mode):
        if access_mode == mpx.MPxFileTranslator.kExportActiveAccessMode:
            om1.MGlobal.displayError("Export Selection is not yet implemented.")
            return

        self._export_geo = True
        self._export_lights = True
        self._export_normals = True
        self._export_uv = True

        om1.MGlobal.displayInfo(options_string)
        self._parse_command_options(options_string)
        self._get_render_globals()

        base_path = file_object.expandedFullName()

        for frame in range(self._start_frame, self._end_frame + 1, self._frame_step):
            oma2.MAnimControl.setCurrentTime(om2.MTime(frame, om2.MTime.uiUnit()))

            om1.MGlobal.displayInfo(f"Exporting frame  {frame:0{self._frame_pad}d}")

            rib_path = f"{base_path}.{frame:0{self._frame_pad}d}.rib"

            try:
                stream = open(rib_path, "w")
            except IOError as exc:
                om1.MGlobal.displayError(f"Error opening file: {rib_path}")
                om1.MGlobal.displayError(str(exc))
                return

            with stream:
                self._stream = stream

                stream.write("# rib export Maya Script \n")
                stream.write(f'Display "{self._image_name}.{frame:0{self._frame_pad}d}.exr" "it" "rgba" \n')
                stream.write(f"Format {self._image_width} {self._image_height} {self._pixel_aspect_ratio:g}\n")

                self._export_camera()
                stream.write("WorldBegin \n")

                if self._export_lights:
                    self._export_all_lights()
                if self._export_geo:
                    self._export_all_meshes()

                stream.write("WorldEnd\n")

            self._stream = None

    # ------------------------------------------------------------------
    # Camera  (API 2.0 – MFnCamera exists there)
    # ------------------------------------------------------------------
    def _export_camera(self):
        it = om2.MItDependencyNodes(om2.MFn.kCamera)
        while not it.isDone():
            node = it.thisNode()
            cam_fn = om2.MFnCamera(node)

            try:
                renderable = cam_fn.findPlug("renderable", False).asBool()
            except Exception:
                renderable = False

            if renderable:
                fl = cam_fn.focalLength
                fov_rad = 2.0 * math.atan((self._image_width / float(self._image_height)) * 12.7 / fl)
                self._stream.write(f'Projection "perspective" "uniform float fov" [{math.degrees(fov_rad):g}]\n')

                dag_fn = om2.MFnDagNode(node)
                dag_path = dag_fn.getPath()
                tx_inv = dag_path.inclusiveMatrixInverse()

                self._stream.write("Identity \n")
                self._stream.write("# camera tx \n")
                self._stream.write("Scale 1 1 -1 \n")
                self._stream.write("ConcatTransform [ ")
                for row in range(4):
                    for col in range(4):
                        self._stream.write(f" {tx_inv.getElement(row, col):g} ")
                self._stream.write(" ]\n")
                return

            it.next()

    # ------------------------------------------------------------------
    # Lights  (API 1.0 – MFnLight/MFnSpotLight etc. missing from API 2.0)
    # ------------------------------------------------------------------
    def _export_all_lights(self):
        it = om1.MItDependencyNodes(om1.MFn.kLight)
        while not it.isDone():
            self._export_light(it.thisNode())
            it.next()

    def _export_light(self, node):
        """Export a single light as a RIB LightSource (API 1.0)."""
        dag_fn = om1.MFnDagNode(node)

        # Colour
        try:
            color_plug = dag_fn.findPlug("color")
            r = color_plug.child(0).asFloat()
            g = color_plug.child(1).asFloat()
            b = color_plug.child(2).asFloat()
        except Exception:
            r, g, b = 1.0, 1.0, 1.0

        # Intensity
        try:
            intensity = dag_fn.findPlug("intensity").asFloat()
        except Exception:
            intensity = 1.0

        # World matrix via dag path
        try:
            dag_path = dag_fn.getPath()
        except Exception:
            om1.MGlobal.displayWarning(f"Could not get dag path for light: {dag_fn.name()}")
            return

        world_mtx = dag_path.inclusiveMatrix()
        pos_x = world_mtx[3 * 4 + 0]
        pos_y = world_mtx[3 * 4 + 1]
        pos_z = world_mtx[3 * 4 + 2]
        dir_x = -world_mtx[2 * 4 + 0]
        dir_y = -world_mtx[2 * 4 + 1]
        dir_z = -world_mtx[2 * 4 + 2]

        node_type = node.apiType()

        if node_type == om1.MFn.kSpotLight:
            spot_fn = om1.MFnSpotLight(node)
            cone_angle = spot_fn.coneAngle()
            penumbra = spot_fn.penumbraAngle()
            self._stream.write(
                f'LightSource "spotlight" 1 '
                f'"intensity" [{intensity:g}] '
                f'"lightcolor" [{r:g} {g:g} {b:g}] '
                f'"from" [{pos_x:g} {pos_y:g} {pos_z:g}] '
                f'"to" [{pos_x + dir_x:g} {pos_y + dir_y:g} {pos_z + dir_z:g}] '
                f'"coneangle" [{cone_angle:g}] '
                f'"conedeltaangle" [{penumbra:g}]\n'
            )

        elif node_type == om1.MFn.kDirectionalLight:
            self._stream.write(
                f'LightSource "distantlight" 1 '
                f'"intensity" [{intensity:g}] '
                f'"lightcolor" [{r:g} {g:g} {b:g}] '
                f'"from" [{pos_x - dir_x:g} {pos_y - dir_y:g} {pos_z - dir_z:g}] '
                f'"to" [{pos_x:g} {pos_y:g} {pos_z:g}]\n'
            )

        elif node_type == om1.MFn.kAmbientLight:
            self._stream.write(
                f'LightSource "ambientlight" 1 "intensity" [{intensity:g}] "lightcolor" [{r:g} {g:g} {b:g}]\n'
            )

        else:
            # Default: point light
            self._stream.write(
                f'LightSource "pointlight" 1 '
                f'"intensity" [{intensity:g}] '
                f'"lightcolor" [{r:g} {g:g} {b:g}] '
                f'"from" [{pos_x:g} {pos_y:g} {pos_z:g}]\n'
            )

    # ------------------------------------------------------------------
    # Meshes  (API 2.0)
    # ------------------------------------------------------------------
    def _export_all_meshes(self):
        it = om2.MItDependencyNodes(om2.MFn.kMesh)
        while not it.isDone():
            self._export_mesh(it.thisNode())
            it.next()

    def _export_mesh(self, node):
        """Export a single mesh as RIB Polygon primitives (API 2.0)."""
        mesh = om2.MFnMesh(node)

        if mesh.isIntermediateObject:
            return

        self._stream.write("TransformBegin\n")
        self._stream.write("Identity \n")

        dag_fn = om2.MFnDagNode(node)
        dag_path = dag_fn.getPath()
        tx = dag_path.inclusiveMatrix()

        self._stream.write(f"# exporting maya mesh {mesh.name()}\n")
        self._stream.write("ConcatTransform [ ")
        for row in range(4):
            for col in range(4):
                self._stream.write(f" {tx.getElement(row, col):g} ")
        self._stream.write(" ]\n")

        vts = mesh.getPoints(om2.MSpace.kObject)
        nmls = mesh.getNormals(om2.MSpace.kObject)

        uv_set_names = mesh.getUVSetNames()
        has_uvs = len(uv_set_names) > 0 and mesh.numUVs() > 0
        if has_uvs:
            u_array, v_array = mesh.getUVs()

        it_poly = om2.MItMeshPolygon(node)
        while not it_poly.isDone():
            vc = it_poly.polygonVertexCount()
            self._stream.write("Polygon ")

            self._stream.write('"vertex point P" [')
            for i in range(vc):
                p = vts[it_poly.vertexIndex(i)]
                self._stream.write(f"{p.x:g} {p.y:g} {p.z:g} ")
            self._stream.write("] ")

            if self._export_normals:
                self._stream.write('"varying normal N" [')
                for i in range(vc):
                    n = nmls[it_poly.normalIndex(i)]
                    self._stream.write(f"{n.x:g} {n.y:g} {n.z:g} ")
                self._stream.write("] ")

            if has_uvs and self._export_uv:
                self._stream.write('"varying float[2] st" [')
                for i in range(vc):
                    idx = it_poly.getUVIndex(i)
                    self._stream.write(f"{u_array[idx]:g} {v_array[idx]:g} ")
                self._stream.write("] ")

            self._stream.write("\n")
            it_poly.next()

        self._stream.write("TransformEnd\n")

    # ------------------------------------------------------------------
    # Render globals  (API 1.0 – MCommonRenderSettingsData missing from 2.0)
    # ------------------------------------------------------------------
    def _get_render_globals(self):
        data = omr.MCommonRenderSettingsData()
        omr.MRenderUtil.getCommonRenderSettings(data)

        self._start_frame = int(data.frameStart.value())
        self._end_frame = int(data.frameEnd.value())
        self._frame_step = int(data.frameBy)
        self._image_name = cmds.getAttr("defaultRenderGlobals.imageFilePrefix") or "noNameSet"
        self._pixel_aspect_ratio = data.pixelAspectRatio
        self._image_width = data.width
        self._image_height = data.height
        self._frame_pad = data.framePadding

        if not self._image_name:
            om1.MGlobal.displayWarning("No filename set in render globals, using default.")
            self._image_name = "noNameSet"

    # ------------------------------------------------------------------
    # Option string parser
    # ------------------------------------------------------------------
    def _parse_command_options(self, options_string):
        if not options_string:
            return

        for item in options_string.split(";"):
            if "=" not in item:
                continue
            key, _, val = item.partition("=")
            key = key.strip()
            om1.MGlobal.displayInfo(key)
            flag = val.strip() not in ("0", "false", "False", "")

            if key == "-normals":
                self._export_normals = flag
            elif key == "-uvs":
                self._export_uv = flag
            elif key == "-geo":
                self._export_geo = flag
            elif key == "-lights":
                self._export_lights = flag

    # ------------------------------------------------------------------
    # Creator
    # ------------------------------------------------------------------
    @staticmethod
    def creator():
        return mpx.asMPxPtr(RibExport())


# ===========================================================================
# Plugin registration
# ===========================================================================
def initializePlugin(plugin):
    plugin_fn = mpx.MFnPlugin(plugin, PLUGIN_VENDOR, PLUGIN_VERSION, "Any")
    try:
        plugin_fn.registerFileTranslator(
            PLUGIN_NAME,
            "none",
            RibExport.creator,
            OPTION_SCRIPT,
            DEFAULT_OPTIONS,
        )
    except Exception as exc:
        sys.stderr.write(f"Failed to register '{PLUGIN_NAME}': {exc}\n")
        raise


def uninitializePlugin(plugin):
    plugin_fn = mpx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterFileTranslator(PLUGIN_NAME)
    except Exception as exc:
        sys.stderr.write(f"Failed to deregister '{PLUGIN_NAME}': {exc}\n")
        raise
