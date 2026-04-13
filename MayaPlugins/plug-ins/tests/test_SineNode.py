import math
import os
import sys

import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.standalone
import pytest
import SineNode

NODE_NAME = "TestSineNode"
PLUGIN_NAME = "SineNode.py"
NODE_TYPE = "SineNodePy"


@pytest.fixture(scope="module")
def load_plugin(maya_standalone):
    cmds.loadPlugin(PLUGIN_NAME)
    cmds.createNode(NODE_TYPE, name=NODE_NAME)
    yield
    # new file to clear all nodes
    cmds.file(new=True, force=True)
    cmds.unloadPlugin(PLUGIN_NAME)


def test_SineNodeCreated(load_plugin):
    assert cmds.objExists(NODE_NAME)
    assert cmds.nodeType(NODE_NAME) == NODE_TYPE


def test_defaultOutput(load_plugin):
    result = cmds.getAttr(f"{NODE_NAME}.output")
    assert result == pytest.approx(0.0)
    result = cmds.getAttr(f"{NODE_NAME}.amplitude")
    assert result == pytest.approx(1.0)
    result = cmds.getAttr(f"{NODE_NAME}.frequency")
    assert result == pytest.approx(1.0)
    result = cmds.getAttr(f"{NODE_NAME}.time")
    assert result == pytest.approx(0.0)
    result = cmds.getAttr(f"{NODE_NAME}.functionType")
    assert result == 0


def test_setAttrib(load_plugin):

    amplitude = 2.0
    frequency = 200.0
    time = OpenMaya.MTime(1.0, OpenMaya.MTime.kSeconds)

    # Set the amplitude attribute
    cmds.setAttr(f"{NODE_NAME}.amplitude", amplitude)
    result = cmds.getAttr(f"{NODE_NAME}.amplitude")
    assert result == pytest.approx(2.0)

    cmds.setAttr(f"{NODE_NAME}.frequency", frequency)
    result = cmds.getAttr(f"{NODE_NAME}.frequency")
    assert result == pytest.approx(frequency)
    cmds.connectAttr("time1.outTime", f"{NODE_NAME}.time")
    # Set the current time in frames so time1.outTime matches our expected value
    # At default 24fps, 1 second = 24 frames
    fps = {"film": 24, "pal": 25, "ntsc": 30}.get(
        cmds.currentUnit(query=True, time=True), 24
    )
    cmds.currentTime(
        time.asUnits(OpenMaya.MTime.kSeconds) * fps, edit=True, update=True
    )

    result = cmds.getAttr(f"{NODE_NAME}.output")

    value = amplitude * math.sin(
        math.radians(frequency * math.pi * time.asUnits(OpenMaya.MTime.kSeconds))
    )

    assert result == pytest.approx(value)
    # test cos
    cmds.setAttr(f"{NODE_NAME}.functionType", 1)
    result = cmds.getAttr(f"{NODE_NAME}.output")
    value = amplitude * math.cos(
        math.radians(frequency * math.pi * time.asUnits(OpenMaya.MTime.kSeconds))
    )
    assert result == pytest.approx(value)
    # complex
    cmds.setAttr(f"{NODE_NAME}.functionType", 2)
    result = cmds.getAttr(f"{NODE_NAME}.output")
    value = amplitude * math.sin(
        math.radians(frequency * math.pi * time.asUnits(OpenMaya.MTime.kSeconds))
    ) + amplitude * math.sin(
        math.radians(2 * frequency * math.pi * time.asUnits(OpenMaya.MTime.kSeconds))
    )
    assert result == pytest.approx(value)
