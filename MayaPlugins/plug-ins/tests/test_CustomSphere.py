def test_CustomSphere(maya_standalone):
    # Create a sphere
    #
    import maya.cmds as cmds

    print("loading plugin")
    cmds.loadPlugin("CustomSphere.py")
    cmds.CustomSpherePy(100)
    results = cmds.ls("sphere*", type="shape")
    assert len(results) == 100
    cmds.undo()
    results = cmds.ls("sphere*", type="shape")
    assert len(results) == 0
