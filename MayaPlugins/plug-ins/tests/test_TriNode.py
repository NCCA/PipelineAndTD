import os
import sys

import maya.cmds as cmds
import maya.standalone
import pytest
import SineNode

NODE_NAME = "TestSineNode"
PLUGIN_NAME = "TriLocatorNode.py"
NODE_TYPE = "TriLocatorNode"


@pytest.fixture(scope="module")
def load_plugin(maya_standalone):
    cmds.loadPlugin(PLUGIN_NAME)
    cmds.createNode(NODE_TYPE, name=NODE_NAME)
    yield
    # new file to clear all nodes
    cmds.file(new=True, force=True)
    cmds.unloadPlugin(PLUGIN_NAME)


def test_tri_node(load_plugin):
    assert cmds.objExists(NODE_NAME)
    assert cmds.nodeType(NODE_NAME) == NODE_TYPE
    assert cmds.getAttr(f"{NODE_NAME}.size") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.size", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.size") == pytest.approx(2.0)
