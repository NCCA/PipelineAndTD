import os
import sys

import CustomSphereSolution
import maya.standalone
import pytest


def test_CustomSphere(maya_standalone):
    # Create a sphere
    #
    import maya.cmds as cmds

    print("loading plugin")
    cmds.loadPlugin("CustomSphereSolution.py")
    cmds.CustomSphereSolutionPy(n=100, x=20, y=20, z=20, mr=0.2, mm=2.5)
    results = cmds.ls("sphere*", type="shape")
    assert len(results) == 100
    cmds.undo()
    results = cmds.ls("sphere*", type="shape")
    assert len(results) == 0
