#!/usr/bin/env python

import json

with open('scene.json') as f:
    scene = json.load(f)

print(scene)