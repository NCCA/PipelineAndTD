
import maya.cmds as cmds
import pytest

NODE_NAME = "TestNoiseNode"
PLUGIN_NAME = "NoiseNode.py"
NODE_TYPE = "NoiseNode"


@pytest.fixture(scope="module")
def load_plugin(maya_standalone):
    cmds.loadPlugin(PLUGIN_NAME)
    cmds.createNode(NODE_TYPE, name=NODE_NAME)
    yield
    # new file to clear all nodes
    cmds.file(new=True, force=True)
    cmds.unloadPlugin(PLUGIN_NAME)


def test_NodeCreated(load_plugin):
    assert cmds.objExists(NODE_NAME)
    assert cmds.nodeType(NODE_NAME) == NODE_TYPE


def test_noise_type(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.noise_type") == pytest.approx(0)
    cmds.setAttr(f"{NODE_NAME}.noise_type", 1)
    assert cmds.getAttr(f"{NODE_NAME}.noise_type") == pytest.approx(1)
    cmds.setAttr(f"{NODE_NAME}.noise_type", 2)
    assert cmds.getAttr(f"{NODE_NAME}.noise_type") == pytest.approx(2)
    with pytest.raises(RuntimeError):
        cmds.setAttr(f"{NODE_NAME}.noise_type", 3)


def test_seed(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.seed") == pytest.approx(1234.0)
    cmds.setAttr(f"{NODE_NAME}.seed", 5678.0)
    assert cmds.getAttr(f"{NODE_NAME}.seed") == pytest.approx(5678.0)


def test_amplitude(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.amplitude") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.amplitude", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.amplitude") == pytest.approx(2.0)


def test_scale(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.scale") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.scale", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.scale") == pytest.approx(2.0)


def test_step(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.step") == pytest.approx(4.0)
    cmds.setAttr(f"{NODE_NAME}.step", 2.0)
    assert cmds.getAttr(f"{NODE_NAME}.step") == pytest.approx(2.0)


def test_persistence(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.persistence") == pytest.approx(1.0)
    cmds.setAttr(f"{NODE_NAME}.persistence", 0.5)
    assert cmds.getAttr(f"{NODE_NAME}.persistence") == pytest.approx(0.5)


def test_position(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.position") == [(0.0, 0.0, 0.0)]
    cmds.setAttr(f"{NODE_NAME}.position", 1.0, 2.0, 3.0)
    assert cmds.getAttr(f"{NODE_NAME}.position") == [(1.0, 2.0, 3.0)]


def test_output(load_plugin):
    assert cmds.getAttr(f"{NODE_NAME}.output") == 0.0
