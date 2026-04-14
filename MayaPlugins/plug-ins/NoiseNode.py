import math
import sys

import maya.api.OpenMaya as OpenMaya
from Noise import Noise

# Set this flag to show we are using api 2.0
maya_useNewAPI = True


class NoiseNode(OpenMaya.MPxNode):
    # class attributes are placed here maya will use these to create the node
    # and to determine the type of node which is setup during initialize method
    # Older plugins used to set these to OpenMaya.MObject() (see api1 demos)
    # however we now just set to None and use the FunctionSets to create the attributes
    id = OpenMaya.MTypeId(0x00105482)
    noise_type = None

    def __init__(self):
        OpenMaya.MPxNode.__init__(self)
        id = OpenMaya.MTypeId(0x00105823)
        seed = None
        amplitude = None
        scale = None
        step = None
        persistence = None
        position = None
        output = None
        noise_type = None
        self.noise = Noise()
        self.seed = 1234.0

    # factory to create the node
    @classmethod
    def creator(cls):
        return cls()

    @classmethod
    def _make_double_attribute(cls, name, short, default_value=0.0, type=OpenMaya.MFnNumericData.kDouble):
        fn = OpenMaya.MFnNumericAttribute()

        if type == OpenMaya.MFnNumericData.k3Double:
            # k3Double needs three child attributes created separately
            fn_x = OpenMaya.MFnNumericAttribute()
            fn_y = OpenMaya.MFnNumericAttribute()
            fn_z = OpenMaya.MFnNumericAttribute()

            # Unpack default, falling back to zeros
            if isinstance(default_value, (list, tuple)) and len(default_value[0]) == 3:
                dx, dy, dz = default_value[0]
            else:
                dx, dy, dz = 0.0, 0.0, 0.0

            attr_x = fn_x.create(f"{name}X", f"{short}x", OpenMaya.MFnNumericData.kDouble, dx)
            attr_y = fn_y.create(f"{name}Y", f"{short}y", OpenMaya.MFnNumericData.kDouble, dy)
            attr_z = fn_z.create(f"{name}Z", f"{short}z", OpenMaya.MFnNumericData.kDouble, dz)

            attr = fn.create(name, short, attr_x, attr_y, attr_z)
        else:
            attr = fn.create(name, short, type, default_value)

        fn.storable = True
        fn.writable = True
        fn.readable = True
        fn.keyable = True
        cls.addAttribute(attr)
        return attr

    @staticmethod
    def initialize():
        # add enum attribute
        enum_attribute_fn = OpenMaya.MFnEnumAttribute()
        NoiseNode.noise_type = enum_attribute_fn.create("noise_type", "nt")
        enum_attribute_fn.addField("Perlin", 0)
        enum_attribute_fn.addField("Turbulence", 1)
        enum_attribute_fn.addField("Complex", 2)

        enum_attribute_fn.storable = True
        enum_attribute_fn.keyable = True
        enum_attribute_fn.readable = True
        OpenMaya.MPxNode.addAttribute(NoiseNode.noise_type)

        NoiseNode.seed = NoiseNode._make_double_attribute("seed", "se", 1234.0)
        NoiseNode.amplitude = NoiseNode._make_double_attribute("amplitude", "amp", 1.0)
        NoiseNode.scale = NoiseNode._make_double_attribute("scale", "sc", 1.0)
        NoiseNode.step = NoiseNode._make_double_attribute("step", "st", 4.0)
        NoiseNode.persistence = NoiseNode._make_double_attribute("persistence", "pe", 1.0)
        NoiseNode.position = NoiseNode._make_double_attribute(
            "position", "pos", [(0.0, 0.0, 0.0)], type=OpenMaya.MFnNumericData.k3Double
        )
        numeric_attrib_fn = OpenMaya.MFnNumericAttribute()
        NoiseNode.output = numeric_attrib_fn.create("output", "o", OpenMaya.MFnNumericData.kDouble, 0.0)
        numeric_attrib_fn.storable = False
        numeric_attrib_fn.keyable = False
        numeric_attrib_fn.readable = True
        numeric_attrib_fn.writable = False
        OpenMaya.MPxNode.addAttribute(NoiseNode.output)
        OpenMaya.MPxNode.attributeAffects(NoiseNode.position, NoiseNode.output)
        OpenMaya.MPxNode.attributeAffects(NoiseNode.seed, NoiseNode.output)
        OpenMaya.MPxNode.attributeAffects(NoiseNode.amplitude, NoiseNode.output)
        OpenMaya.MPxNode.attributeAffects(NoiseNode.scale, NoiseNode.output)
        OpenMaya.MPxNode.attributeAffects(NoiseNode.step, NoiseNode.output)
        OpenMaya.MPxNode.attributeAffects(NoiseNode.persistence, NoiseNode.output)

        return True

    def compute(self, plug, data):
        """
        Description

           When input attributes are dirty this method will be called to
           recompute the output attributes.

        Arguments

           plug      - the attribute that triggered the compute
           data - the nodes data
        """
        # we only need to compute if the plug is the output node changing
        if plug == NoiseNode.output:
            position_data = data.inputValue(NoiseNode.position).asFloatVector()
            seed_data = data.inputValue(NoiseNode.seed).asInt()
            amplitude_data = data.inputValue(NoiseNode.amplitude).asDouble()
            scale_data = data.inputValue(NoiseNode.scale).asDouble()
            step_data = data.inputValue(NoiseNode.step).asDouble()
            persistence_data = data.inputValue(NoiseNode.persistence).asDouble()
            print(
                f"position={position_data}, seed={seed_data}, amplitude={amplitude_data}, scale={scale_data}, step={step_data}, persistence={persistence_data}"
            )
            print(f"{type(position_data)} ")

            # if seed != self.seed:
            #     self.noise.seed(seed)
            #     self.noise.resetTables()
            selected_noise_type = data.inputValue(NoiseNode.noise_type).asInt()
            if selected_noise_type == 0:
                output = self.noise.noise(scale_data, tuple(position_data)) / amplitude_data
            elif selected_noise_type == 1:
                output = self.noise.turbulence(scale_data, tuple(position_data)) / amplitude_data
            elif selected_noise_type == 2:
                output = (
                    self.noise.complex(step_data, persistence_data, scale_data, tuple(position_data)) / amplitude_data
                )
            output_data = data.outputValue(NoiseNode.output)
            output_data.setDouble(output)
            data.setClean(plug)

            return True
        return False


def initializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)
    try:
        plugin.registerNode("NoiseNode", NoiseNode.id, NoiseNode.creator, NoiseNode.initialize)
    except:
        sys.stderr.write("Failed to register node\n")
        raise


def uninitializePlugin(obj):
    plugin = OpenMaya.MFnPlugin(obj)

    try:
        plugin.deregisterNode(NoiseNode.id)
    except:
        sys.stderr.write("Failed to deregister node\n")
        raise
