import os
import sys

import maya.cmds as cmds
import maya.standalone
import pytest
import SineNode

node_name = "TestSineNode"


@pytest.fixture(scope="module")
def setup_module(maya_standalone):
    cmds.loadPlugin("SineNode.py")
    cmds.createNode("SineNodePy", name=node_name)


def test_SineNode(setup_module):
    # Create a sphere
    import maya.cmds as cmds

    results = cmds.ls(node_name)
    assert len(results) == 1


def test_setAttrib(setup_module):
    import maya.cmds as cmds

    # Set the amplitude attribute
    cmds.setAttr(f"{node_name}.amplitude", 2.0)
    results = cmds.getAttr(f"{node_name}.amplitude")
    assert results == pytest.approx(2.0)

    cmds.setAttr(f"{node_name}.frequency", 200.0)
    results = cmds.getAttr(f"{node_name}.frequency")
    assert results == pytest.approx(200.0)
