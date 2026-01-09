#!/usr/bin/env -S uv run --active --script

import json

with open("scene.json") as f:
    scene = json.load(f)

print(scene)
