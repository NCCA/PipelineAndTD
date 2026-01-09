import maya.cmds as cmds
import json
# Create a cube if it doesn't exist

if  cmds.objExists("TestCube"):
    cmds.delete("TestCube")
cmds.polyCube(n="TestCube")

# Add a custom string attribute to the cube for the USD Json dictionary
cmds.addAttr("TestCube", longName="USD_UserExportedAttributesJson",  dataType="string")

attr_json={}
attr_json["CustomFloatValue"] = {"usdAttrName": "CustomFloatValue", "usdAttrType": "float", "usdAttrValue": 1.0}
attr_json["CustomStringValue"] = {"usdAttrName": "CustomStringValue", "usdAttrType": "string", "usdAttrValue": "Hello World"}
attr_json["CustomIntValue"] = {"usdAttrName": "CustomIntValue", "usdAttrType": "int", "usdAttrValue": 10}
attr_json["CustomBoolValue"] = {"usdAttrName": "CustomBoolValue", "usdAttrType": "bool", "usdAttrValue": True}
attr_json["CustomVec3Value"] = {"usdAttrName": "CustomVec3Value", "usdAttrType": "vec3f", "usdAttrValue": [1.0, 2.0, 3.0], "usdAttrValueSize": 3}
attr_json["CustomFloatMatrixValue"] = {"usdAttrName": "CustomFloatMatrixValue", "usdAttrType": "matrix4d", "usdAttrValue": [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0], "usdAttrValueSize": 16}
attr_json["CustomFloatPrimvarArray"] = {"usdAttrName": "CustomFloatPrimvarArray", "usdAttrType": "float[]", "usdAttrValue": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0], "usdAttrValueSize": 6}
# set this json dictionary and the exporter will parse it and set the attributes
cmds.setAttr("TestCube.USD_UserExportedAttributesJson", json.dumps(attr_json), type='string')


# Now set the actual attribute values , they should match the schema above
cmds.addAttr("TestCube", longName="CustomFloatValue",  attributeType="float")
cmds.setAttr("TestCube.CustomFloatValue", 1.0)  

# here is the string one (not the differences)
cmds.addAttr("TestCube", longName="CustomStringValue",  dataType="string")
cmds.setAttr("TestCube.CustomStringValue", "Hello World Again",type="string")  

cmds.addAttr("TestCube", longName="CustomIntValue",  attributeType="long")
cmds.setAttr("TestCube.CustomIntValue", 10)

cmds.addAttr("TestCube", longName="CustomBoolValue",  attributeType="bool")
cmds.setAttr("TestCube.CustomBoolValue", 1)

cmds.addAttr("TestCube", longName="CustomVec3Value",  dataType="float3")
cmds.setAttr("TestCube.CustomVec3Value", 1.0, 2.0, 3.0, type="float3")

cmds.addAttr("TestCube", longName="CustomFloatMatrixValue",  dataType="matrix")
cmds.setAttr("TestCube.CustomFloatMatrixValue", 1.0, 0.0, 0.0, 0.0,
                        0.0, 1.0, 0.0, 0.0,
                        0.0, 0.0, 1.0, 0.0,
                        0.0, 0.0, 0.0, 1.0, type="matrix")

cmds.addAttr("TestCube", longName="CustomFloatPrimvarArray",  dataType="floatArray")
cmds.setAttr("TestCube.CustomFloatPrimvarArray", (1.0, 2.0, 3.0, 4.0, 5.0, 6.0), type="floatArray")

