import os
import sys

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
    import maya.cmds as cmds

    results = cmds.ls(NODE_NAME)
    assert len(results) == 1


def test_setAttrib(load_plugin):
    import maya.cmds as cmds

    # Set the amplitude attribute
    cmds.setAttr(f"{NODE_NAME}.amplitude", 2.0)
    results = cmds.getAttr(f"{NODE_NAME}.amplitude")
    assert results == pytest.approx(2.0)

    cmds.setAttr(f"{NODE_NAME}.frequency", 200.0)
    results = cmds.getAttr(f"{NODE_NAME}.frequency")
    assert results == pytest.approx(200.0)
