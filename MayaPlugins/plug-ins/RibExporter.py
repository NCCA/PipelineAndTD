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

from __future__ import annotations

import math
import sys
from typing import IO, Any, List, Optional, Tuple

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
PLUGIN_NAME: str = "RibExport"
PLUGIN_VERSION: str = "1.0"
PLUGIN_VENDOR: str = "Jon Macey"
OPTION_SCRIPT: str = "RibExportScript"
DEFAULT_OPTIONS: str = ""


# ===========================================================================
class RibExport(mpx.MPxFileTranslator):
    """Writes one RenderMan RIB file per frame over the Render Globals range.

    This translator exports Maya scene geometry, lights, and camera data into
    RenderMan RIB (RenderMan Interface Bytestream) format. It iterates over
    the animation range defined in the Render Globals and produces one RIB
    file per frame.

    Attributes:
        _export_geo: Whether to export mesh geometry.
        _export_lights: Whether to export scene lights.
        _export_normals: Whether to export vertex normals.
        _export_uv: Whether to export UV coordinates.
        _start_frame: First frame of the animation range.
        _end_frame: Last frame of the animation range.
        _frame_step: Frame step interval.
        _frame_pad: Zero-padding width for frame numbers.
        _image_name: Image file prefix from Render Globals.
        _pixel_aspect_ratio: Pixel aspect ratio for the output.
        _image_width: Output image width in pixels.
        _image_height: Output image height in pixels.
        _stream: The active file stream for the current RIB file.
    """

    # ------------------------------------------------------------------
    # MPxFileTranslator interface
    # ------------------------------------------------------------------
    def haveReadMethod(self) -> bool:
        """Return whether this translator supports reading files.

        Returns:
            False — this translator is write-only.
        """
        return False

    def haveWriteMethod(self) -> bool:
        """Return whether this translator supports writing files.

        Returns:
            True — this translator can export RIB files.
        """
        return True

    def defaultExtension(self) -> str:
        """Return the default file extension for this translator.

        Returns:
            The string 'rib'.
        """
        return "rib"

    def filter(self) -> str:
        """Return the file dialog filter pattern.

        Returns:
            The string '*.rib'.
        """
        return "*.rib"

    # ------------------------------------------------------------------
    # writer
    # ------------------------------------------------------------------
    def writer(
        self,
        file_object: om1.MFileObject,
        options_string: str,
        access_mode: int,
    ) -> None:
        """Write the Maya scene to RIB format.

        Iterates over the animation range set in Render Globals, setting the
        current time for each frame and writing a separate RIB file per frame.

        Args:
            file_object: Maya file object containing the target output path.
            options_string: Semicolon-separated option flags (e.g.
                '-normals=1;-uvs=1;-geo=1;-lights=1').
            access_mode: Export access mode flag from MPxFileTranslator.
                kExportActiveAccessMode triggers an error since selection
                export is not yet implemented.
        """
        if access_mode == mpx.MPxFileTranslator.kExportActiveAccessMode:
            om1.MGlobal.displayError("Export Selection is not yet implemented.")
            return

        self._export_geo: bool = True
        self._export_lights: bool = True
        self._export_normals: bool = True
        self._export_uv: bool = True

        om1.MGlobal.displayInfo(options_string)
        self._parse_command_options(options_string)
        self._get_render_globals()

        base_path: str = file_object.expandedFullName()

        for frame in range(self._start_frame, self._end_frame + 1, self._frame_step):
            oma2.MAnimControl.setCurrentTime(om2.MTime(frame, om2.MTime.uiUnit()))

            om1.MGlobal.displayInfo(f"Exporting frame  {frame:0{self._frame_pad}d}")

            rib_path: str = f"{base_path}.{frame:0{self._frame_pad}d}.rib"

            try:
                stream: IO[str] = open(rib_path, "w")
            except IOError as exc:
                om1.MGlobal.displayError(f"Error opening file: {rib_path}")
                om1.MGlobal.displayError(str(exc))
                return

            with stream:
                self._stream: IO[str] = stream

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
    def _export_camera(self) -> None:
        """Find the first renderable camera and write its RIB projection data.

        Computes the vertical field of view from the camera's focal length
        and the output image dimensions, then writes a Perspective projection
        with the camera's inverse world matrix as a ConcatTransform.
        """
        it: om2.MItDependencyNodes = om2.MItDependencyNodes(om2.MFn.kCamera)
        while not it.isDone():
            node: om2.MObject = it.thisNode()
            cam_fn: om2.MFnCamera = om2.MFnCamera(node)

            try:
                renderable: bool = cam_fn.findPlug("renderable", False).asBool()
            except Exception:
                renderable = False

            if renderable:
                fl: float = cam_fn.focalLength
                fov_rad: float = 2.0 * math.atan((self._image_width / float(self._image_height)) * 12.7 / fl)
                self._stream.write(f'Projection "perspective" "uniform float fov" [{math.degrees(fov_rad):g}]\n')

                dag_fn: om2.MFnDagNode = om2.MFnDagNode(node)
                dag_path: om2.MDagPath = dag_fn.getPath()
                tx_inv: om2.MMatrix = dag_path.inclusiveMatrixInverse()

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
    def _export_all_lights(self) -> None:
        """Iterate over all lights in the scene and export each one."""
        it: om1.MItDependencyNodes = om1.MItDependencyNodes(om1.MFn.kLight)
        while not it.isDone():
            self._export_light(it.thisNode())
            it.next()

    def _export_light(self, node: om1.MObject) -> None:
        """Export a single light as a RIB LightSource.

        Determines the light type (spot, directional, ambient, or point)
        and writes the appropriate LightSource call with intensity, colour,
        position, and direction derived from the light's DAG node and world
        matrix.

        Args:
            node: Maya MObject representing the light node.
        """
        dag_fn: om1.MFnDagNode = om1.MFnDagNode(node)

        # Colour
        try:
            color_plug: om1.MPlug = dag_fn.findPlug("color")
            r: float = color_plug.child(0).asFloat()
            g: float = color_plug.child(1).asFloat()
            b: float = color_plug.child(2).asFloat()
        except Exception:
            r, g, b = 1.0, 1.0, 1.0

        # Intensity
        try:
            intensity: float = dag_fn.findPlug("intensity").asFloat()
        except Exception:
            intensity = 1.0

        # World matrix via dag path
        try:
            dag_path: om1.MDagPath = dag_fn.getPath()
        except Exception:
            om1.MGlobal.displayWarning(f"Could not get dag path for light: {dag_fn.name()}")
            return

        world_mtx: om1.MMatrix = dag_path.inclusiveMatrix()
        pos_x: float = world_mtx[3 * 4 + 0]
        pos_y: float = world_mtx[3 * 4 + 1]
        pos_z: float = world_mtx[3 * 4 + 2]
        dir_x: float = -world_mtx[2 * 4 + 0]
        dir_y: float = -world_mtx[2 * 4 + 1]
        dir_z: float = -world_mtx[2 * 4 + 2]

        node_type: int = node.apiType()

        if node_type == om1.MFn.kSpotLight:
            spot_fn: om1.MFnSpotLight = om1.MFnSpotLight(node)
            cone_angle: float = spot_fn.coneAngle()
            penumbra: float = spot_fn.penumbraAngle()
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
    def _export_all_meshes(self) -> None:
        """Iterate over all meshes in the scene and export each one."""
        it: om2.MItDependencyNodes = om2.MItDependencyNodes(om2.MFn.kMesh)
        while not it.isDone():
            self._export_mesh(it.thisNode())
            it.next()

    def _export_mesh(self, node: om2.MObject) -> None:
        """Export a single mesh as RIB Polygon primitives.

        Writes a TransformBegin/TransformEnd block with the mesh's world
        matrix, then iterates over each face writing Polygon primitives with
        vertex positions and optionally normals and UV coordinates.

        Intermediate (history) objects are skipped.

        Args:
            node: Maya MObject representing the mesh node.
        """
        mesh: om2.MFnMesh = om2.MFnMesh(node)

        if mesh.isIntermediateObject:
            return

        self._stream.write("TransformBegin\n")
        self._stream.write("Identity \n")

        dag_fn: om2.MFnDagNode = om2.MFnDagNode(node)
        dag_path: om2.MDagPath = dag_fn.getPath()
        tx: om2.MMatrix = dag_path.inclusiveMatrix()

        self._stream.write(f"# exporting maya mesh {mesh.name()}\n")
        self._stream.write("ConcatTransform [ ")
        for row in range(4):
            for col in range(4):
                self._stream.write(f" {tx.getElement(row, col):g} ")
        self._stream.write(" ]\n")

        vts: om2.MPointArray = mesh.getPoints(om2.MSpace.kObject)
        nmls: om2.MVectorArray = mesh.getNormals(om2.MSpace.kObject)

        uv_set_names: List[str] = mesh.getUVSetNames()
        has_uvs: bool = len(uv_set_names) > 0 and mesh.numUVs() > 0
        if has_uvs:
            u_array: List[float]
            v_array: List[float]
            u_array, v_array = mesh.getUVs()

        it_poly: om2.MItMeshPolygon = om2.MItMeshPolygon(node)
        while not it_poly.isDone():
            vc: int = it_poly.polygonVertexCount()
            self._stream.write("Polygon ")

            self._stream.write('"vertex point P" [')
            for i in range(vc):
                p: om2.MPoint = vts[it_poly.vertexIndex(i)]
                self._stream.write(f"{p.x:g} {p.y:g} {p.z:g} ")
            self._stream.write("] ")

            if self._export_normals:
                self._stream.write('"varying normal N" [')
                for i in range(vc):
                    n: om2.MVector = nmls[it_poly.normalIndex(i)]
                    self._stream.write(f"{n.x:g} {n.y:g} {n.z:g} ")
                self._stream.write("] ")

            if has_uvs and self._export_uv:
                self._stream.write('"varying float[2] st" [')
                for i in range(vc):
                    idx: int = it_poly.getUVIndex(i)
                    self._stream.write(f"{u_array[idx]:g} {v_array[idx]:g} ")
                self._stream.write("] ")

            self._stream.write("\n")
            it_poly.next()

        self._stream.write("TransformEnd\n")

    # ------------------------------------------------------------------
    # Render globals  (API 1.0 – MCommonRenderSettingsData missing from 2.0)
    # ------------------------------------------------------------------
    def _get_render_globals(self) -> None:
        """Read render settings from Maya and populate frame/image attributes.

        Queries MCommonRenderSettingsData for the animation range, frame
        padding, image dimensions, and pixel aspect ratio. Reads the image
        file prefix from defaultRenderGlobals.imageFilePrefix.
        """
        data: omr.MCommonRenderSettingsData = omr.MCommonRenderSettingsData()
        omr.MRenderUtil.getCommonRenderSettings(data)

        self._start_frame: int = int(data.frameStart.value())
        self._end_frame: int = int(data.frameEnd.value())
        self._frame_step: int = int(data.frameBy)
        self._image_name: str = cmds.getAttr("defaultRenderGlobals.imageFilePrefix") or "noNameSet"
        self._pixel_aspect_ratio: float = data.pixelAspectRatio
        self._image_width: int = data.width
        self._image_height: int = data.height
        self._frame_pad: int = data.framePadding

        if not self._image_name:
            om1.MGlobal.displayWarning("No filename set in render globals, using default.")
            self._image_name = "noNameSet"

    # ------------------------------------------------------------------
    # Option string parser
    # ------------------------------------------------------------------
    def _parse_command_options(self, options_string: str) -> None:
        """Parse the semicolon-separated option string into export flags.

        Recognised keys are -normals, -uvs, -geo, and -lights.  A value of
        '0', 'false', 'False', or empty string disables the flag; any other
        value enables it.

        Args:
            options_string: Semicolon-separated key=value pairs, e.g.
                '-normals=1;-uvs=1;-geo=1;-lights=1'.
        """
        if not options_string:
            return

        for item in options_string.split(";"):
            if "=" not in item:
                continue
            key: str
            val: str
            key, _, val = item.partition("=")
            key = key.strip()
            om1.MGlobal.displayInfo(key)
            flag: bool = val.strip() not in ("0", "false", "False", "")

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
    def creator() -> Any:
        """Create and return an instance of this translator.

        Returns:
            A pointer to a new RibExport instance wrapped via asMPxPtr.
        """
        return mpx.asMPxPtr(RibExport())


# ===========================================================================
# Plugin registration
# ===========================================================================
def initializePlugin(plugin: om1.MObject) -> None:
    """Register the RibExport file translator with Maya.

    Args:
        plugin: MObject representing the loaded plugin provided by Maya.

    Raises:
        Exception: If the translator registration fails.
    """
    plugin_fn: mpx.MFnPlugin = mpx.MFnPlugin(plugin, PLUGIN_VENDOR, PLUGIN_VERSION, "Any")
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


def uninitializePlugin(plugin: om1.MObject) -> None:
    """Deregister the RibExport file translator from Maya.

    Args:
        plugin: MObject representing the loaded plugin provided by Maya.

    Raises:
        Exception: If the translator deregistration fails.
    """
    plugin_fn: mpx.MFnPlugin = mpx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterFileTranslator(PLUGIN_NAME)
    except Exception as exc:
        sys.stderr.write(f"Failed to deregister '{PLUGIN_NAME}': {exc}\n")
        raise
