import os
import sys

import maya.cmds as cmds
import maya.standalone
import pytest
import SineNode

NODE_NAME = "TestCubeNode"
PLUGIN_NAME = "CubeLocatorNode.py"
NODE_TYPE = "CubeLocatorNode"


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


def test_att_width(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.width") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.width", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.width") == pytest.approx(2.0)


def test_att_depth(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.depth") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.depth", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.depth") == pytest.approx(2.0)


def test_att_height(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.height") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.height", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.height") == pytest.approx(2.0)


def test_volume(load_plugin):
    cmds.setAttr(f"{NODE_NAME}.width", 2.0)
    cmds.setAttr(f"{NODE_NAME}.depth", 2.0)
    cmds.setAttr(f"{NODE_NAME}.height", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.volume") == pytest.approx(8.0)


def test_colour(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.colour") == [(1.0, 1.0, 1.0)]
    cmds.setAttr(f"{NODE_NAME}.colour", 0.0, 0.0, 0.0)
    assert cmds.getAttr(f"{NODE_NAME}.colour") == [(0.0, 0.0, 0.0)]


def test_text_colour(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.textColour") == [(1.0, 1.0, 1.0)]
    cmds.setAttr(f"{NODE_NAME}.textColour", 0.0, 0.0, 0.0)
    assert cmds.getAttr(f"{NODE_NAME}.textColour") == [(0.0, 0.0, 0.0)]
