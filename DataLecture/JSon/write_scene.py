#!/usr/bin/env python

import json
from jsonschema import validate

with open('scene_schema.json') as f:
    schema = json.load(f)

scene={}

scene["scene_name"] = "test_scene"
scene["meshes"] = []

# add mesh
mesh = {}
mesh["name"] = "test_mesh"
mesh["path"] = "1.obj"
mesh["position"] = { "x"  : 0, "y" :  0, "z" : 0}
scene["meshes"].append(mesh)


validate(instance=scene, schema=schema)


with open('scene.json', 'w') as f:
    json.dump(scene, f, indent=4)